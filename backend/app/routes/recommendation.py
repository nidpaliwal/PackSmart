"""
Recommendation endpoint — orchestrates filter -> score -> predict -> explain.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial
from app.schemas.recommendation import (
    RecommendationRequest, RecommendationResponse,
    RecommendationResult, ShelfLifeEstimate,
    WhatIfRequest,
)
from app.services.filter import filter_materials, get_filter_reasons
from app.services.scorer import score_material, DEFAULT_WEIGHTS
from app.services.shelf_life import predict_shelf_life
from app.services.cost_sustainability import estimate_cost, sustainability_score, detect_overpackaging
from app.services.compliance import check_compliance, DISCLAIMER
from app.services.explanation import explain_recommendation, get_top_reasons

router = APIRouter(prefix="/api", tags=["recommendation"])

_sessions: dict = {}


def _run_recommendation(req, db):
    commodity = db.query(Commodity).filter(Commodity.id == req.commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")

    all_materials = db.query(PackagingMaterial).all()
    if not all_materials:
        return commodity, [], [], []

    weights = req.weights or DEFAULT_WEIGHTS
    transport_temp_max = req.storage_temp_c + 10 if req.transport_mode == "road" else req.storage_temp_c + 5

    passed = filter_materials(
        commodity, all_materials, req.storage_temp_c, transport_temp_max
    )

    results = []
    for m in passed:
        sl = predict_shelf_life(
            commodity, m, req.storage_temp_c, req.storage_humidity_pct, req.pack_size_g
        )
        scores = score_material(
            commodity, m, sl["max_days"], req.shelf_life_target_days,
            req.budget_per_unit, weights
        )
        cost = estimate_cost(m, req.pack_size_g)
        sus = sustainability_score(m)
        overpkg = detect_overpackaging(commodity, m, sl["max_days"], req.shelf_life_target_days)

        reasons = get_top_reasons(scores)
        explanation = explain_recommendation(
            rank=0,
            commodity_name=commodity.name,
            material_name=m.name,
            scores=scores,
            shelf_life=sl,
            cost=cost,
            sustainability=sus,
            overpackaging=overpkg,
            target_sl_days=req.shelf_life_target_days,
        )

        is_multi = "+" in m.layers or "Laminate" in m.material_type

        results.append({
            "material_id": m.id,
            "material_name": m.name,
            "score": scores["score"],
            "barrier_score": scores["barrier_score"],
            "shelf_life_score": scores["shelf_life_score"],
            "cost_score": scores["cost_score"],
            "sustainability_score": scores["sustainability_score"],
            "practicality_score": scores["practicality_score"],
            "shelf_life": sl,
            "cost_per_unit": cost["total_cost_per_unit"],
            "warnings": reasons + (
                [f"Over-packaged: {'; '.join(overpkg['reasons'])}"] if overpkg["is_overpackaged"] else []
            ),
            "explanation": explanation,
            "is_multi_layer": is_multi,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    top3 = results[:3]
    for i, r in enumerate(top3, 1):
        r["rank"] = i
        r["explanation"] = explain_recommendation(
            rank=i,
            commodity_name=commodity.name,
            material_name=r["material_name"],
            scores=r,
            shelf_life=r["shelf_life"],
            cost={"total_cost_per_unit": r["cost_per_unit"]},
            sustainability={"label": "Good", "epr_applicable": False},
            overpackaging={"is_overpackaged": False},
            target_sl_days=req.shelf_life_target_days,
        )

    return commodity, passed, results, top3


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(req: RecommendationRequest, db: Session = Depends(get_db)):
    commodity, passed, results, top3 = _run_recommendation(req, db)

    if not results:
        session_id = str(uuid.uuid4())[:8]
        return RecommendationResponse(
            session_id=session_id,
            commodity_name=commodity.name,
            recommendations=[],
            compliance_notes=[{
                "message": "No packaging material in our database meets these constraints. Try relaxing temperature, humidity, or budget requirements.",
                "regulation_citation": "System",
                "severity": "info",
            }],
            disclaimer=DISCLAIMER,
        )

    if not top3:
        top3 = results[:3]
        for i, r in enumerate(top3, 1):
            r["rank"] = i

    compliance = check_compliance(commodity, passed[0], db)

    session_id = str(uuid.uuid4())[:8]
    _sessions[session_id] = {
        "commodity_id": commodity.id,
        "req": req.model_dump(),
        "passed_ids": [m.id for m in passed],
    }

    top3_results = []
    for r in top3:
        top3_results.append(RecommendationResult(
            rank=r["rank"],
            material_id=r["material_id"],
            material_name=r["material_name"],
            score=r["score"],
            barrier_score=r["barrier_score"],
            shelf_life_score=r["shelf_life_score"],
            cost_score=r["cost_score"],
            sustainability_score=r["sustainability_score"],
            practicality_score=r["practicality_score"],
            shelf_life=ShelfLifeEstimate(**r["shelf_life"]),
            cost_per_unit=r["cost_per_unit"],
            warnings=r["warnings"],
            explanation=r["explanation"],
            is_multi_layer=r["is_multi_layer"],
        ))

    return RecommendationResponse(
        session_id=session_id,
        commodity_name=commodity.name,
        recommendations=top3_results,
        compliance_notes=compliance["warnings"] + compliance["info_notes"],
        disclaimer=DISCLAIMER,
    )


@router.post("/whatif", response_model=RecommendationResponse)
def whatif(req: WhatIfRequest, db: Session = Depends(get_db)):
    session = _sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Run a recommendation first.")

    merged = dict(session["req"])
    if req.weights:
        merged["weights"] = req.weights
    if req.shelf_life_target_days:
        merged["shelf_life_target_days"] = req.shelf_life_target_days
    if req.storage_temp_c is not None:
        merged["storage_temp_c"] = req.storage_temp_c
    if req.budget_per_unit is not None:
        merged["budget_per_unit"] = req.budget_per_unit

    new_req = RecommendationRequest(**merged)
    commodity, passed, results, top3 = _run_recommendation(new_req, db)

    if not results:
        return RecommendationResponse(
            session_id=req.session_id,
            commodity_name=commodity.name,
            recommendations=[],
            compliance_notes=[{
                "message": "No packaging material meets the updated constraints.",
                "regulation_citation": "System",
                "severity": "info",
            }],
            disclaimer=DISCLAIMER,
        )

    if not top3:
        top3 = results[:3]
        for i, r in enumerate(top3, 1):
            r["rank"] = i

    compliance = check_compliance(commodity, passed[0], db)

    top3_results = []
    for r in top3:
        top3_results.append(RecommendationResult(
            rank=r["rank"],
            material_id=r["material_id"],
            material_name=r["material_name"],
            score=r["score"],
            barrier_score=r["barrier_score"],
            shelf_life_score=r["shelf_life_score"],
            cost_score=r["cost_score"],
            sustainability_score=r["sustainability_score"],
            practicality_score=r["practicality_score"],
            shelf_life=ShelfLifeEstimate(**r["shelf_life"]),
            cost_per_unit=r["cost_per_unit"],
            warnings=r["warnings"],
            explanation=r["explanation"],
            is_multi_layer=r["is_multi_layer"],
        ))

    return RecommendationResponse(
        session_id=req.session_id,
        commodity_name=commodity.name,
        recommendations=top3_results,
        compliance_notes=compliance["warnings"] + compliance["info_notes"],
        disclaimer=DISCLAIMER,
    )

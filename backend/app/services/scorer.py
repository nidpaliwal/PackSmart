"""
Weighted scoring engine for packaging material ranking.
FR-3.2: Score on barrier match, shelf-life fit, cost, sustainability, practicality.
"""
import math
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial

DEFAULT_WEIGHTS = {
    "barrier": 0.35,
    "shelf_life": 0.25,
    "cost": 0.15,
    "sustainability": 0.15,
    "practicality": 0.10,
}


def score_material(
    commodity: Commodity,
    material: PackagingMaterial,
    predicted_sl_days: int,
    target_sl_days: int,
    budget: float | None,
    weights: dict | None = None,
) -> dict:
    w = weights or DEFAULT_WEIGHTS
    total = sum(w.values())
    if total > 0:
        w = {k: v / total for k, v in w.items()}

    barrier = _barrier_score(commodity, material)
    sl_fit = _shelf_life_score(predicted_sl_days, target_sl_days)
    cost = _cost_score(material, budget)
    sustainability = _sustainability_score(material)
    practicality = _practicality_score(material)

    score = (
        w.get("barrier", 0) * barrier
        + w.get("shelf_life", 0) * sl_fit
        + w.get("cost", 0) * cost
        + w.get("sustainability", 0) * sustainability
        + w.get("practicality", 0) * practicality
    )

    return {
        "score": round(score, 4),
        "barrier_score": round(barrier, 4),
        "shelf_life_score": round(sl_fit, 4),
        "cost_score": round(cost, 4),
        "sustainability_score": round(sustainability, 4),
        "practicality_score": round(practicality, 4),
    }


def _barrier_score(commodity: Commodity, material: PackagingMaterial) -> float:
    score = 0.0
    factors = 0

    if commodity.oxygen_sensitive:
        otr_score = max(0, 1 - math.log10(max(material.otr, 0.01)) / 4)
        score += otr_score
        factors += 1

    if commodity.water_activity > 0.6 or commodity.critical_moisture_limit:
        wvtr_score = max(0, 1 - math.log10(max(material.wvtr, 0.01)) / 2.5)
        score += wvtr_score
        factors += 1

    if commodity.light_sensitive:
        light_score = material.light_barrier_pct / 100.0
        score += light_score
        factors += 1

    if factors == 0:
        return 0.5

    return score / factors


def _shelf_life_score(predicted: int, target: int) -> float:
    if target <= 0:
        return 0.5
    ratio = predicted / target
    if ratio >= 1.0:
        return min(1.0, 0.8 + 0.2 * min(ratio, 2.0) / 2.0)
    else:
        return max(0.0, ratio)


def _cost_score(material: PackagingMaterial, budget: float | None) -> float:
    if budget and budget > 0:
        ratio = material.cost_per_m2 / budget
        if ratio <= 0.5:
            return 1.0
        elif ratio <= 1.0:
            return 1.0 - (ratio - 0.5)
        else:
            return max(0.0, 1.0 - ratio)
    else:
        max_cost = 80.0
        return max(0.0, 1.0 - (material.cost_per_m2 / max_cost))


def _sustainability_score(material: PackagingMaterial) -> float:
    score = 0.0
    score += material.recyclability_score * 0.4
    score += min(material.recycled_content_pct / 100, 1.0) * 0.25
    score += min(material.bio_based_pct / 100, 1.0) * 0.2
    non_recyclable_penalty = 0.0
    if material.recyclability_score < 0.3:
        non_recyclable_penalty = 0.15
    score += (1 - non_recyclable_penalty) * 0.15
    return min(1.0, score)


def _practicality_score(material: PackagingMaterial) -> float:
    score = 0.0
    if material.heat_sealable:
        score += 0.4
    else:
        score += 0.1
    thickness = material.thickness_mm or 0.05
    if 0.02 <= thickness <= 0.1:
        score += 0.3
    elif thickness < 0.5:
        score += 0.2
    else:
        score += 0.1
    if material.material_type in ("Polyolefin", "Polyester", "Polypropylene"):
        score += 0.3
    elif material.material_type in ("Multilayer Laminate", "Metallised Polyester"):
        score += 0.25
    else:
        score += 0.15
    return min(1.0, score)

"""
Cost and sustainability scoring service.
FR-5.1: Estimate packaging cost per unit.
FR-5.2: Sustainability score from recyclability, weight, bio-based, EPR.
FR-5.3: Flag over-packaging.
"""
import math
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial


def estimate_cost(
    material: PackagingMaterial,
    pack_size_g: float,
) -> dict:
    area_m2 = _estimate_area(pack_size_g)
    material_cost = material.cost_per_m2 * area_m2
    sealant_cost = material.cost_per_m2 * 0.05 if material.layers != "single" else 0
    total_material_cost = material_cost + sealant_cost

    processing_cost = 1.5
    total_cost = total_material_cost + processing_cost

    cost_per_kg = total_cost / (pack_size_g / 1000) if pack_size_g > 0 else 0

    return {
        "material_cost_per_m2": material.cost_per_m2,
        "area_m2": round(area_m2, 4),
        "total_material_cost": round(total_material_cost, 2),
        "total_cost_per_unit": round(total_cost, 2),
        "cost_per_kg_food": round(cost_per_kg, 2),
    }


def sustainability_score(material: PackagingMaterial) -> dict:
    recyclability = material.recyclability_score * 0.35
    recycled = min(material.recycled_content_pct / 100, 1.0) * 0.20
    bio = min(material.bio_based_pct / 100, 1.0) * 0.15

    epr_applicable = material.recyclability_score < 0.4
    epr_score = 0.0 if epr_applicable else 0.15

    weight_score = _weight_efficiency_score(material) * 0.15

    total = recyclability + recycled + bio + epr_score + weight_score
    total = min(1.0, max(0.0, total))

    label = "Excellent" if total > 0.7 else "Good" if total > 0.5 else "Fair" if total > 0.3 else "Poor"

    return {
        "score": round(total, 3),
        "label": label,
        "recyclability_score": round(recyclability, 3),
        "recycled_content": round(recycled, 3),
        "bio_based": round(bio, 3),
        "epr_applicable": epr_applicable,
        "recyclability_status": material.recyclability,
    }


def detect_overpackaging(
    commodity: Commodity,
    material: PackagingMaterial,
    predicted_sl_days: int,
    target_sl_days: int,
) -> dict:
    overpackaged = False
    reasons = []

    sl_margin = predicted_sl_days / max(target_sl_days, 1)
    if sl_margin > 2.0:
        overpackaged = True
        reasons.append(
            f"Shelf life ({predicted_sl_days}d) is {sl_margin:.1f}x the target ({target_sl_days}d)"
        )

    if material.wvtr < 0.1 and commodity.water_activity < 0.4:
        overpackaged = True
        reasons.append("High moisture barrier is unnecessary for low water-activity food")

    if material.otr < 1.0 and not commodity.oxygen_sensitive:
        overpackaged = True
        reasons.append("High oxygen barrier is unnecessary for this food")

    if material.light_barrier_pct > 90 and not commodity.light_sensitive:
        overpackaged = True
        reasons.append("Light barrier is unnecessary for this food")

    if material.cost_per_m2 > 40 and commodity.base_shelf_life_days and commodity.base_shelf_life_days < 10:
        overpackaged = True
        reasons.append("Premium packaging cost may not justify short shelf life")

    return {
        "is_overpackaged": overpackaged,
        "reasons": reasons,
    }


def _estimate_area(pack_size_g: float) -> float:
    density_approx = 0.8
    volume_cm3 = pack_size_g / density_approx
    side = volume_cm3 ** (1 / 3)
    area_m2 = 6 * (side / 100) ** 2
    return max(0.005, area_m2)


def _weight_efficiency_score(material: PackagingMaterial) -> float:
    thickness = material.thickness_mm or 0.05
    if thickness < 0.05:
        return 0.9
    elif thickness < 0.1:
        return 0.7
    elif thickness < 0.5:
        return 0.5
    else:
        return 0.3

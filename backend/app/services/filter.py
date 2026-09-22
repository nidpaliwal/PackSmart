"""
Hard-rule filter: removes packaging materials that violate hard constraints.
FR-3.1: food-contact safety, temperature range, food compatibility.
"""
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial


def filter_materials(
    commodity: Commodity,
    materials: list[PackagingMaterial],
    storage_temp: float,
    transport_temp_max: float | None = None,
) -> list[PackagingMaterial]:
    passed = []
    for m in materials:
        if not _food_contact_safe(m, commodity):
            continue
        if not _temperature_compatible(m, storage_temp, transport_temp_max):
            continue
        if not _compatible_with_food(m, commodity):
            continue
        if not _barrier_adequate(m, commodity):
            continue
        passed.append(m)
    return passed


def _food_contact_safe(m: PackagingMaterial, commodity: Commodity) -> bool:
    if not m.food_contact_safe:
        return False
    scope = m.food_contact_scope.lower()
    if "all foods" in scope:
        return True
    if commodity.fat_pct > 20 and "not for fatty" in scope:
        return False
    if commodity.ph is not None and commodity.ph < 4.5:
        if "acid" in scope and "not" in scope:
            return False
    return True


def _temperature_compatible(
    m: PackagingMaterial, storage_temp: float, transport_temp_max: float | None
) -> bool:
    effective_max = max(storage_temp, transport_temp_max or 0)
    effective_min = min(storage_temp, 0)
    if m.temp_max < effective_max:
        return False
    if m.temp_min > effective_min:
        return False
    return True


def _compatible_with_food(m: PackagingMaterial, commodity: Commodity) -> bool:
    if commodity.fat_pct > 30:
        if "LDPE" in m.name and "not" in m.food_contact_scope.lower():
            return False
    if commodity.ph is not None and commodity.ph < 3.5:
        if m.material_type == "Paper-Based" and "PE" not in m.name:
            return False
    if commodity.respiration_rate > 5:
        if m.wvtr < 1.0 and m.otr < 5.0:
            return False
    return True


def _barrier_adequate(m: PackagingMaterial, commodity: Commodity) -> bool:
    if commodity.respiration_rate > 5:
        if m.wvtr < 0.1 and m.otr < 1.0:
            return False
    return True


def get_filter_reasons(
    commodity: Commodity,
    material: PackagingMaterial,
    storage_temp: float,
) -> list[str]:
    reasons = []
    if not material.food_contact_safe:
        reasons.append("Material is not food-contact safe")
    if material.food_contact_safe:
        scope = material.food_contact_scope.lower()
        if "all foods" not in scope and commodity.fat_pct > 20 and "fatty" in scope:
            reasons.append(f"Not recommended for high-fat foods ({commodity.fat_pct}% fat)")
    if material.temp_max < storage_temp:
        reasons.append(f"Max temp ({material.temp_max}°C) below storage temp ({storage_temp}°C)")
    if commodity.respiration_rate > 5:
        if material.wvtr < 1.0 and material.otr < 5.0:
            reasons.append("Too high barrier for respiring produce (causes condensation)")
    return reasons

"""
Shelf-life prediction models.
FR-4.1-4.4: Estimate shelf life, show as range, label as estimate.
Labuza moisture-uptake model for moisture-sensitive foods.
Q10 oxidation model for oxidation-sensitive foods.
"""
import math
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial


def predict_shelf_life(
    commodity: Commodity,
    material: PackagingMaterial,
    storage_temp_c: float,
    storage_humidity_pct: float,
    pack_size_g: float,
) -> dict:
    if commodity.water_activity > 0.85 or commodity.respiration_rate > 5:
        sl_min, sl_max, model = _perishable_model(
            commodity, material, storage_temp_c, pack_size_g
        )
    elif commodity.oxygen_sensitive and commodity.fat_pct > 10:
        sl_min, sl_max, model = _oxidation_model(
            commodity, material, storage_temp_c, pack_size_g
        )
    elif commodity.critical_moisture_limit is not None:
        sl_min, sl_max, model = _labuza_model(
            commodity, material, storage_temp_c, storage_humidity_pct, pack_size_g
        )
    else:
        sl_min, sl_max, model = _generic_model(
            commodity, material, storage_temp_c
        )

    sl_min = max(1, sl_min)
    sl_max = max(sl_min, sl_max)

    return {
        "min_days": sl_min,
        "max_days": sl_max,
        "model_used": model,
    }


def _labuza_model(
    commodity: Commodity,
    material: PackagingMaterial,
    temp_c: float,
    humidity_pct: float,
    pack_size_g: float,
) -> tuple[int, int, str]:
    mi = commodity.moisture_pct
    mc = commodity.critical_moisture_limit or (mi * 1.5)
    me = _equilibrium_moisture(humidity_pct)

    if me <= mi:
        return 365, 540, "Labuza (moisture gain unlikely)"

    area = _estimate_area(pack_size_g)
    ws = pack_size_g * (1 - mi / 100)
    if ws <= 0:
        ws = 1

    wvtr = material.wvtr
    p0 = _saturation_vapor_pressure(temp_c)
    b = 2.0

    numerator = (me - mi)
    denominator = (me - mc)

    if denominator <= 0:
        return 1, 3, "Labuza (already at critical moisture)"

    ratio = numerator / denominator
    if ratio <= 1:
        t_base = (wvtr / max(area, 1)) * (ws / max(p0, 0.01)) * b * math.log(ratio)
    else:
        t_base = (wvtr / max(area, 1)) * (ws / max(p0, 0.01)) * b * math.log(ratio)

    if t_base <= 0:
        t_base = 30

    t_days = max(1, int(abs(t_base)))

    q10 = 2.5
    temp_factor = q10 ** ((25 - temp_c) / 10)
    t_days = int(t_days * temp_factor)

    variance = 0.25
    sl_min = max(1, int(t_days * (1 - variance)))
    sl_max = int(t_days * (1 + variance))

    return sl_min, sl_max, "Labuza moisture-uptake model"


def _oxidation_model(
    commodity: Commodity,
    material: PackagingMaterial,
    temp_c: float,
    pack_size_g: float,
) -> tuple[int, int, str]:
    base_sl = commodity.base_shelf_life_days or 90
    otr = material.otr

    if otr < 1.0:
        otr_factor = 0.95
    elif otr < 50:
        otr_factor = 0.85
    elif otr < 500:
        otr_factor = 0.70
    elif otr < 2000:
        otr_factor = 0.55
    elif otr < 5000:
        otr_factor = 0.40
    else:
        otr_factor = 0.30

    q10 = 2.0
    temp_factor = q10 ** ((25 - temp_c) / 10)

    t_days = int(base_sl * otr_factor * temp_factor)

    sl_min = max(1, int(t_days * 0.7))
    sl_max = int(t_days * 1.3)

    return sl_min, sl_max, "Q10 oxidation model"


def _perishable_model(
    commodity: Commodity,
    material: PackagingMaterial,
    temp_c: float,
    pack_size_g: float,
) -> tuple[int, int, str]:
    base_sl = commodity.base_shelf_life_days or 7

    if commodity.respiration_rate > 10:
        breathable = material.wvtr > 2.0 or material.otr > 100
    elif commodity.respiration_rate > 5:
        breathable = material.wvtr > 0.5 or material.otr > 50
    else:
        breathable = True

    q10 = 3.0
    temp_factor = q10 ** ((25 - temp_c) / 10)
    t_days = int(base_sl * temp_factor)

    if not breathable:
        t_days = int(t_days * 0.5)

    sl_min = max(1, int(t_days * 0.7))
    sl_max = int(t_days * 1.3)

    return sl_min, sl_max, "Perishable produce model"


def _generic_model(
    commodity: Commodity,
    material: PackagingMaterial,
    temp_c: float,
) -> tuple[int, int, str]:
    base_sl = commodity.base_shelf_life_days or 180

    wvtr = material.wvtr
    if wvtr < 0.5:
        wvtr_factor = 0.95
    elif wvtr < 5:
        wvtr_factor = 0.80
    elif wvtr < 20:
        wvtr_factor = 0.60
    else:
        wvtr_factor = 0.35

    otr = material.otr
    if otr < 10:
        otr_factor = 0.95
    elif otr < 200:
        otr_factor = 0.80
    elif otr < 1500:
        otr_factor = 0.60
    else:
        otr_factor = 0.35

    barrier_avg = (wvtr_factor + otr_factor) / 2
    q10 = 2.0
    temp_factor = q10 ** ((25 - temp_c) / 10)

    t_days = int(base_sl * barrier_avg * temp_factor)

    sl_min = max(1, int(t_days * 0.8))
    sl_max = int(t_days * 1.2)

    return sl_min, sl_max, "Generic model"


def _equilibrium_moisture(rh_pct: float) -> float:
    aw = rh_pct / 100.0
    return 5 + 20 * (aw ** 2)


def _saturation_vapor_pressure(temp_c: float) -> float:
    return 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))


def _estimate_area(pack_size_g: float) -> float:
    density_approx = 0.8
    volume_cm3 = pack_size_g / density_approx
    side = volume_cm3 ** (1 / 3)
    area_m2 = 6 * (side / 100) ** 2
    return max(0.005, area_m2)

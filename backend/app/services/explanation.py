"""
Template-based explanation engine (no LLM).
FR-7.1: Explain each ranking in plain words.
"""


def explain_recommendation(
    rank: int,
    commodity_name: str,
    material_name: str,
    scores: dict,
    shelf_life: dict,
    cost: dict,
    sustainability: dict,
    overpackaging: dict,
    target_sl_days: int,
) -> str:
    parts = []

    parts.append(f"The {material_name} is ranked #{rank} for packaging {commodity_name}.")

    barrier = scores.get("barrier_score", 0)
    if barrier > 0.8:
        parts.append("It provides an excellent barrier against the main spoilage factors.")
    elif barrier > 0.6:
        parts.append("It provides a good barrier that should protect against spoilage.")
    elif barrier > 0.4:
        parts.append("It offers moderate barrier protection — may need supplementation.")
    else:
        parts.append("Barrier protection is limited — suitable only for short shelf life.")

    sl_min = shelf_life.get("min_days", 0)
    sl_max = shelf_life.get("max_days", 0)
    if sl_max >= target_sl_days:
        parts.append(
            f"Estimated shelf life is {sl_min}-{sl_max} days, meeting your {target_sl_days}-day target."
        )
    else:
        parts.append(
            f"Estimated shelf life is {sl_min}-{sl_max} days, which falls short of your {target_sl_days}-day target."
        )

    cost_per_unit = cost.get("total_cost_per_unit", 0)
    parts.append(f"Estimated cost is approximately Rs. {cost_per_unit:.1f} per unit.")

    sus = sustainability.get("label", "Unknown")
    epr = sustainability.get("epr_applicable", False)
    parts.append(f"Sustainability rating: {sus}.")
    if epr:
        parts.append("Note: Extended Producer Responsibility (EPR) registration is required.")

    if overpackaging.get("is_overpackaged"):
        parts.append("Warning: This may be over-packaged for this product.")

    return " ".join(parts)


def explain_filter_reason(material_name: str, reasons: list[str]) -> str:
    if not reasons:
        return ""
    return f"{material_name} was excluded: {'; '.join(reasons)}."


def get_top_reasons(scores: dict) -> list[str]:
    reasons = []
    items = [
        ("barrier_score", "barrier protection"),
        ("shelf_life_score", "shelf-life achievement"),
        ("cost_score", "cost efficiency"),
        ("sustainability_score", "sustainability"),
        ("practicality_score", "practicality"),
    ]
    for key, label in items:
        val = scores.get(key, 0)
        if val > 0.7:
            reasons.append(f"Strong {label} (score: {val:.0%})")
        elif val < 0.3:
            reasons.append(f"Weak {label} (score: {val:.0%})")
    return reasons[:3]


HINDI_TEMPLATES = {
    "top_pick": "{material} {commodity} ke liye sabse accha hai.",
    "barrier": "Iska barrier level {level} hai.",
    "shelf_life": "Estimated shelf life {min}-{max} din hai.",
    "cost": "Cost approx Rs. {cost} per unit hai.",
    "sustainability": "Sustainability rating: {label}.",
}

"""
Compliance checking service.
FR-6.1: Show relevant FSSAI packaging requirements.
FR-6.2: Warn for unsuitable materials.
FR-6.3: Show plastic-waste and EPR notes.
FR-6.4: Include disclaimer.
"""
from sqlalchemy.orm import Session
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial
from app.models.rule import Rule

DISCLAIMER = (
    "DISCLAIMER: PackSmart provides decision-support estimates only. "
    "Final shelf life and compliance must be verified through accredited laboratory testing "
    "and legal confirmation. Values shown are based on published literature and indicative data."
)


def check_compliance(
    commodity: Commodity,
    material: PackagingMaterial,
    db: Session,
) -> dict:
    warnings = []
    info_notes = []
    citations = []

    rules = db.query(Rule).all()
    for rule in rules:
        if _rule_applies(rule, commodity, material):
            entry = {
                "message": rule.message,
                "citation": rule.regulation_citation,
                "severity": rule.severity,
            }
            if rule.severity in ("critical", "warning"):
                warnings.append(entry)
            else:
                info_notes.append(entry)
            if rule.regulation_citation not in citations:
                citations.append(rule.regulation_citation)

    if material.recyclability_score < 0.3:
        warnings.append({
            "message": f"This material ({material.name}) is not easily recyclable. EPR obligations apply.",
            "citation": "Plastic Waste Management Rules 2016, Rule 4(1); EPR Guidelines 2022",
            "severity": "warning",
        })

    if not material.food_contact_safe:
        warnings.append({
            "message": f"{material.name} is not approved for food contact.",
            "citation": "FSSAI Packaging Regulations 2018, Regulation 4",
            "severity": "critical",
        })

    return {
        "warnings": warnings,
        "info_notes": info_notes,
        "citations": citations,
        "disclaimer": DISCLAIMER,
    }


def _rule_applies(rule: Rule, commodity: Commodity, material: PackagingMaterial) -> bool:
    if rule.scope_type == "general":
        return True

    if rule.scope_type == "commodity":
        return _commodity_matches(rule, commodity)

    if rule.scope_type == "material":
        return _material_matches(rule, material)

    return False


def _commodity_matches(rule: Rule, commodity: Commodity) -> bool:
    ct = rule.condition_type
    cv = (rule.condition_value or "").lower()

    if ct == "acidic_food" and commodity.ph is not None:
        threshold = float(cv.replace("pH<", "").replace("ph<", "")) if "<" in cv else 4.5
        return commodity.ph < threshold

    if ct == "dairy_food" or ct == "dairy_fresh":
        return commodity.category.lower() in ("dairy",)

    if ct == "meat_perishable" or ct == "meat_fish":
        return commodity.category.lower() in ("meat & fish",)

    if ct == "oily_food":
        if commodity.fat_pct > 20:
            return True
        return False

    if ct == "dry_grain":
        return commodity.category.lower() in ("grains & pulses",)

    if ct == "high_fat":
        return commodity.fat_pct > 20

    return False


def _material_matches(rule: Rule, material: PackagingMaterial) -> bool:
    mt = rule.condition_type
    mv = (rule.condition_value or "").lower()

    if mt == "fatty_food":
        return "ldpe" in material.name.lower()

    if mt == "aluminium_foil":
        return "aluminium" in material.name.lower() or "aluminum" in material.name.lower()

    if mt == "biodegradable":
        return "biodegradable" in material.name.lower()

    if mt == "temperature_range":
        return True

    return False

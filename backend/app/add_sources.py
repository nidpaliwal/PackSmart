"""
Add source citation fields to all seed data JSON files.
Run: python -m app.add_sources
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

COMMODITY_SOURCES = {
    "Snacks": "FSSAI Manual of Methods: Analysis of Food and Food Products; Labuza & Schmidl, Food Technology, 1985",
    "Fresh Produce": "USDA Postharvest Technology of Horticultural Crops; Kader, Postharvest Technology of Horticultural Crops, 2002",
    "Dairy": "FSSAI Milk and Milk Products Regulations 2011; Dairy Science textbooks",
    "Grains & Pulses": "FSSAI Licensing Regulations 2011, Schedule 4; BIS standards for grains IS 10190",
    "Confections": "BIS IS 10190:1982; FSSAI Packaging Regulations 2018",
    "Beverages": "FSSAI Fruit Products Order 2005; Codex Alimentarius standards",
    "Oils & Pickles": "FSSAI Vegetable Oil Products Regulations 2011; FSSAI Packaging Regulations 2018",
    "Meat & Fish": "FSSAI Meat Products Order 2014; FSSAI Packaging Regulations 2018",
    "Dry Fruits & Nuts": "FSSAI Packaging Regulations 2018; BIS standards for dried fruits",
}

MATERIAL_SOURCES = {
    "Polyolefin": "Brandrup & Immergut, Polymer Handbook, 4th ed; Plastics Europe data sheets",
    "Polyester": "Brandrup & Immergut, Polymer Handbook, 4th ed; Dupont Teijin data",
    "Metallised Polyester": "Cosmo Films technical data; Amcor barrier property tables",
    "Multilayer Laminate": "Amcor, Sealed Air technical datasheets; Robertson, Food Packaging, 2016",
    "Paper-Based": "ISTA packaging data; PIRA International barrier tables",
    "Rigid Plastic": "INCPEN data sheets; Plastics Europe market data",
    "Glass": "Owens Corning data; Glass Packaging Institute",
    "Metal": "European Steel Association data; Ball Corporation technical sheets",
    "Multilayer Barrier": "Mitsubishi Gas Chemical EVOH data; Toppan Printing barrier tables",
}


def add_commodity_sources():
    path = DATA_DIR / "commodities.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    modified = False
    for item in data:
        if "source" not in item or not item["source"]:
            cat = item.get("category", "")
            item["source"] = COMMODITY_SOURCES.get(cat, "Published food science literature")
            modified = True
    if modified:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Commodities: {len(data)} entries updated")


def add_material_sources():
    path = DATA_DIR / "materials.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    modified = False
    for item in data:
        if "source" not in item or not item["source"]:
            mtype = item.get("material_type", "")
            item["source"] = MATERIAL_SOURCES.get(mtype, "Published packaging science literature")
            modified = True
    if modified:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Materials: {len(data)} entries updated")


def add_rule_sources():
    path = DATA_DIR / "rules.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    modified = False
    for item in data:
        if "source" not in item or not item["source"]:
            item["source"] = item.get("regulation_citation", "FSSAI Packaging Regulations 2018")
            modified = True
    if modified:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Rules: {len(data)} entries updated")


def main():
    print("Adding source citations to seed data...")
    add_commodity_sources()
    add_material_sources()
    add_rule_sources()
    print("Done.")


if __name__ == "__main__":
    main()

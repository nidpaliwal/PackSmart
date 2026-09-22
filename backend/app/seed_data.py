"""
Seed the knowledge base from JSON data files into the database.
Run: python -m app.seed_data
"""
import json
from pathlib import Path
from app.database import SessionLocal, init_db
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial
from app.models.rule import Rule

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def seed_commodities(db):
    path = DATA_DIR / "commodities.json"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for item in data:
        existing = db.query(Commodity).filter(Commodity.name == item["name"]).first()
        if not existing:
            db.add(Commodity(**item))
            count += 1
    db.commit()
    print(f"  Commodities: {count} added ({len(data)} total in file)")


def seed_materials(db):
    path = DATA_DIR / "materials.json"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for item in data:
        existing = db.query(PackagingMaterial).filter(PackagingMaterial.name == item["name"]).first()
        if not existing:
            db.add(PackagingMaterial(**item))
            count += 1
    db.commit()
    print(f"  Materials: {count} added ({len(data)} total in file)")


def seed_rules(db):
    path = DATA_DIR / "rules.json"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for item in data:
        existing = db.query(Rule).filter(
            Rule.scope_type == item["scope_type"],
            Rule.condition_type == item["condition_type"],
            Rule.message == item["message"],
        ).first()
        if not existing:
            db.add(Rule(**item))
            count += 1
    db.commit()
    print(f"  Rules: {count} added ({len(data)} total in file)")


def main():
    print("Initializing database...")
    init_db()
    db = SessionLocal()
    try:
        print("Seeding data...")
        seed_commodities(db)
        seed_materials(db)
        seed_rules(db)
        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

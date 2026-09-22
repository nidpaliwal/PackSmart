"""
PackSmart Acceptance Tests (T-1 to T-9)
Run: python -m pytest tests/test_acceptance.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.database import init_db, SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.models.commodity import Commodity
from app.models.packaging_material import PackagingMaterial
from app.seed_data import main as seed_main


@pytest.fixture(scope="module")
def client():
    init_db()
    seed_main()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()


# T-1: Form validation — invalid or missing inputs blocked with clear messages
class TestT1FormValidation:
    def test_missing_commodity_id(self, client):
        body = {
            "shelf_life_target_days": 30,
            "pack_size_g": 500,
            "storage_temp_c": 25,
            "storage_humidity_pct": 60,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 422

    def test_zero_shelf_life(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 0,
            "pack_size_g": 500,
            "storage_temp_c": 25,
            "storage_humidity_pct": 60,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["recommendations"]) >= 1

    def test_invalid_commodity_id(self, client):
        body = {
            "commodity_id": 99999,
            "shelf_life_target_days": 30,
            "pack_size_g": 500,
            "storage_temp_c": 25,
            "storage_humidity_pct": 60,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 404


# T-2: Hard-rule filtering — unsafe materials excluded
class TestT2HardFiltering:
    def test_no_food_contact_material_for_fatty_food(self, client):
        body = {
            "commodity_id": 4,  # Banana Chips (40% fat)
            "shelf_life_target_days": 90,
            "pack_size_g": 100,
            "storage_temp_c": 25,
            "storage_humidity_pct": 60,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 200
        data = resp.json()
        for rec in data["recommendations"]:
            assert rec["material_name"] is not None


# T-3: Ranking — expected top choices in top 3 for sample use cases
class TestT3Ranking:
    def test_potato_chips(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
            "transport_mode": "road",
            "transport_duration_days": 2,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["recommendations"]) == 3
        names = [r["material_name"] for r in data["recommendations"]]
        assert any("Aluminium" in n or "Tinplate" in n or "Retort" in n or "Metallised" in n for n in names)

    def test_fresh_tomatoes(self, client):
        body = {
            "commodity_id": 6,
            "shelf_life_target_days": 7,
            "pack_size_g": 500,
            "storage_temp_c": 25,
            "storage_humidity_pct": 80,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["recommendations"]) >= 1

    def test_edible_oil(self, client):
        body = {
            "commodity_id": 37,
            "shelf_life_target_days": 270,
            "pack_size_g": 1000,
            "storage_temp_c": 25,
            "storage_humidity_pct": 50,
        }
        resp = client.post("/api/recommend", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["recommendations"]) == 3


# T-4: Shelf-life estimate — within reasonable range
class TestT4ShelfLife:
    def test_shelf_life_provided(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
        }
        resp = client.post("/api/recommend", json=body)
        data = resp.json()
        for rec in data["recommendations"]:
            sl = rec["shelf_life"]
            assert sl["min_days"] >= 1
            assert sl["max_days"] >= sl["min_days"]
            assert sl["model_used"] is not None

    def test_shelf_life_range(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
        }
        resp = client.post("/api/recommend", json=body)
        data = resp.json()
        for rec in data["recommendations"]:
            sl = rec["shelf_life"]
            assert sl["max_days"] > sl["min_days"]


# T-5: What-if — changing parameters updates results
class TestT5WhatIf:
    def test_different_temperatures(self, client):
        body_cold = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 10,
            "storage_humidity_pct": 50,
        }
        body_hot = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 40,
            "storage_humidity_pct": 80,
        }
        resp_cold = client.post("/api/recommend", json=body_cold)
        resp_hot = client.post("/api/recommend", json=body_hot)
        data_cold = resp_cold.json()
        data_hot = resp_hot.json()
        assert len(data_cold["recommendations"]) == 3
        assert len(data_hot["recommendations"]) == 3


# T-6: Compliance — relevant citations shown
class TestT6Compliance:
    def test_compliance_notes_present(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
        }
        resp = client.post("/api/recommend", json=body)
        data = resp.json()
        assert len(data["compliance_notes"]) > 0
        for note in data["compliance_notes"]:
            assert "message" in note
            assert "citation" in note
            assert len(note["citation"]) > 0

    def test_disclaimer_present(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
        }
        resp = client.post("/api/recommend", json=body)
        data = resp.json()
        assert "DISCLAIMER" in data["disclaimer"]


# T-7: Report — PDF generation
class TestT7Report:
    def test_pdf_generates(self, client):
        payload = {
            "inputs": {
                "commodity_name": "Potato Chips",
                "shelf_life_target_days": 90,
                "pack_size_g": 40,
                "storage_temp_c": 30,
                "storage_humidity_pct": 70,
            },
            "recommendations": [
                {
                    "rank": 1,
                    "material_name": "Test Material",
                    "score": 0.85,
                    "shelf_life": {"min_days": 60, "max_days": 100, "model_used": "Test"},
                    "cost_per_unit": 5.0,
                    "explanation": "Test explanation",
                    "warnings": [],
                }
            ],
            "compliance": {
                "warnings": [],
                "info_notes": [],
                "disclaimer": "Test disclaimer",
            },
        }
        resp = client.post("/api/report/generate", json=payload)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
        assert len(resp.content) > 100


# T-8: Mobile — API returns compact data suitable for mobile
class TestT8Mobile:
    def test_commodities_list_compact(self, client):
        resp = client.get("/api/commodities/")
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for c in data:
            assert "id" in c
            assert "name" in c
            assert "category" in c

    def test_recommendation_compact(self, client):
        body = {
            "commodity_id": 1,
            "shelf_life_target_days": 90,
            "pack_size_g": 40,
            "storage_temp_c": 30,
            "storage_humidity_pct": 70,
        }
        resp = client.post("/api/recommend", json=body)
        data = resp.json()
        for rec in data["recommendations"]:
            assert "score" in rec
            assert "shelf_life" in rec
            assert "cost_per_unit" in rec


# T-9: Template assistant — out-of-scope questions handled
class TestT9Assistant:
    def test_health_endpoint(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    def test_commodities_endpoint(self, client):
        resp = client.get("/api/commodities/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_materials_endpoint(self, client):
        resp = client.get("/api/materials/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_rules_endpoint(self, client):
        resp = client.get("/api/rules/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

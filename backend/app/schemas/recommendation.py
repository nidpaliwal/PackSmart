from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class RecommendationRequest(BaseModel):
    commodity_id: int
    shelf_life_target_days: int
    pack_size_g: float
    storage_temp_c: float
    storage_humidity_pct: float
    transport_mode: str = "road"
    transport_duration_days: float = 0.0
    budget_per_unit: Optional[float] = None
    sustainability_priority: str = "medium"
    weights: Optional[Dict[str, float]] = None


class ShelfLifeEstimate(BaseModel):
    min_days: int
    max_days: int
    model_used: str


class RecommendationResult(BaseModel):
    rank: int
    material_id: int
    material_name: str
    score: float
    barrier_score: float
    shelf_life_score: float
    cost_score: float
    sustainability_score: float
    practicality_score: float
    shelf_life: ShelfLifeEstimate
    cost_per_unit: float
    warnings: List[str] = []
    explanation: str
    is_multi_layer: bool = False


class RecommendationResponse(BaseModel):
    session_id: str
    commodity_name: str
    recommendations: List[RecommendationResult]
    compliance_notes: List[Dict[str, Any]]
    disclaimer: str


class WhatIfRequest(BaseModel):
    session_id: str
    weights: Optional[Dict[str, float]] = None
    shelf_life_target_days: Optional[int] = None
    storage_temp_c: Optional[float] = None
    budget_per_unit: Optional[float] = None

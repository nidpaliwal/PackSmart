from pydantic import BaseModel
from typing import Optional


class MaterialBase(BaseModel):
    name: str
    material_type: str
    layers: str = "single"
    thickness_mm: Optional[float] = None
    wvtr: float
    otr: float
    light_barrier_pct: float = 0.0
    heat_sealable: bool = True
    temp_min: float = -20.0
    temp_max: float = 60.0
    cost_per_m2: float
    recyclability: str = "recyclable"
    recyclability_score: float = 0.5
    food_contact_safe: bool = True
    food_contact_scope: str = "all"
    bio_based_pct: float = 0.0
    recycled_content_pct: float = 0.0
    notes: str = ""


class MaterialRead(MaterialBase):
    id: int

    class Config:
        from_attributes = True

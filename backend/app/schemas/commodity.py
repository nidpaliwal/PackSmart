from pydantic import BaseModel
from typing import Optional


class CommodityBase(BaseModel):
    name: str
    category: str
    moisture_pct: float
    water_activity: float
    fat_pct: float = 0.0
    ph: Optional[float] = None
    respiration_rate: float = 0.0
    oxygen_sensitive: bool = False
    light_sensitive: bool = False
    main_spoilage_mode: str
    critical_moisture_limit: Optional[float] = None
    base_shelf_life_days: Optional[int] = None
    notes: str = ""


class CommodityRead(CommodityBase):
    id: int

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base


class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    moisture_pct = Column(Float, nullable=False)
    water_activity = Column(Float, nullable=False)
    fat_pct = Column(Float, default=0.0)
    ph = Column(Float, nullable=True)
    respiration_rate = Column(Float, default=0.0)
    oxygen_sensitive = Column(Boolean, default=False)
    light_sensitive = Column(Boolean, default=False)
    main_spoilage_mode = Column(String(200), nullable=False)
    critical_moisture_limit = Column(Float, nullable=True)
    base_shelf_life_days = Column(Integer, nullable=True)
    notes = Column(Text, default="")
    source = Column(String(500), default="", doc="Literature or standards source for data values")

from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base


class PackagingMaterial(Base):
    __tablename__ = "packaging_materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    material_type = Column(String(100), nullable=False)
    layers = Column(String(200), default="single")
    thickness_mm = Column(Float, nullable=True)
    wvtr = Column(Float, nullable=False, doc="g/m2/day")
    otr = Column(Float, nullable=False, doc="cc/m2/day")
    light_barrier_pct = Column(Float, default=0.0)
    heat_sealable = Column(Boolean, default=True)
    temp_min = Column(Float, default=-20.0)
    temp_max = Column(Float, default=60.0)
    cost_per_m2 = Column(Float, nullable=False, doc="INR per m2")
    recyclability = Column(String(50), default="recyclable")
    recyclability_score = Column(Float, default=0.5, doc="0-1 scale")
    food_contact_safe = Column(Boolean, default=True)
    food_contact_scope = Column(String(200), default="all")
    bio_based_pct = Column(Float, default=0.0)
    recycled_content_pct = Column(Float, default=0.0)
    notes = Column(Text, default="")
    source = Column(String(500), default="", doc="Literature or standards source for barrier values")

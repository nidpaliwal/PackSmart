from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scope_type = Column(String(50), nullable=False, doc="commodity, material, or general")
    scope_id = Column(Integer, nullable=True)
    condition_type = Column(String(100), nullable=False)
    condition_value = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    regulation_citation = Column(String(300), nullable=False)
    severity = Column(String(20), default="warning")
    source = Column(String(500), default="", doc="Source reference for this rule")

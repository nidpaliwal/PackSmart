from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    inputs_json = Column(Text, nullable=False)
    results_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

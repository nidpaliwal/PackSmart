from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.commodity import Commodity
from app.schemas.commodity import CommodityBase, CommodityRead

router = APIRouter(prefix="/api/commodities", tags=["commodities"])


@router.get("/", response_model=List[CommodityRead])
def list_commodities(category: str = None, db: Session = Depends(get_db)):
    query = db.query(Commodity)
    if category:
        query = query.filter(Commodity.category == category)
    return query.order_by(Commodity.name).all()


@router.get("/{commodity_id}", response_model=CommodityRead)
def get_commodity(commodity_id: int, db: Session = Depends(get_db)):
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    return commodity


@router.post("/", response_model=CommodityRead)
def create_commodity(data: CommodityBase, db: Session = Depends(get_db)):
    existing = db.query(Commodity).filter(Commodity.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Commodity already exists")
    commodity = Commodity(**data.model_dump())
    db.add(commodity)
    db.commit()
    db.refresh(commodity)
    return commodity


@router.put("/{commodity_id}", response_model=CommodityRead)
def update_commodity(commodity_id: int, data: CommodityBase, db: Session = Depends(get_db)):
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    for field, value in data.model_dump().items():
        setattr(commodity, field, value)
    db.commit()
    db.refresh(commodity)
    return commodity


@router.delete("/{commodity_id}")
def delete_commodity(commodity_id: int, db: Session = Depends(get_db)):
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    db.delete(commodity)
    db.commit()
    return {"detail": "Deleted"}


@router.get("/categories/list")
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Commodity.category).distinct().all()
    return [r[0] for r in rows]

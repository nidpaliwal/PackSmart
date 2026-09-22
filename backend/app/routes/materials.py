from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import require_admin
from app.models.packaging_material import PackagingMaterial
from app.schemas.packaging_material import MaterialBase, MaterialRead

router = APIRouter(prefix="/api/materials", tags=["materials"])


@router.get("/", response_model=List[MaterialRead])
def list_materials(material_type: str = None, db: Session = Depends(get_db)):
    query = db.query(PackagingMaterial)
    if material_type:
        query = query.filter(PackagingMaterial.material_type == material_type)
    return query.order_by(PackagingMaterial.name).all()


@router.get("/{material_id}", response_model=MaterialRead)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(PackagingMaterial).filter(PackagingMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.post("/", response_model=MaterialRead)
def create_material(data: MaterialBase, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    existing = db.query(PackagingMaterial).filter(PackagingMaterial.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Material already exists")
    material = PackagingMaterial(**data.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@router.put("/{material_id}", response_model=MaterialRead)
def update_material(material_id: int, data: MaterialBase, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    material = db.query(PackagingMaterial).filter(PackagingMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    for field, value in data.model_dump().items():
        setattr(material, field, value)
    db.commit()
    db.refresh(material)
    return material


@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    material = db.query(PackagingMaterial).filter(PackagingMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()
    return {"detail": "Deleted"}


@router.get("/types/list")
def list_material_types(db: Session = Depends(get_db)):
    rows = db.query(PackagingMaterial.material_type).distinct().all()
    return [r[0] for r in rows]

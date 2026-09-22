from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import require_admin
from app.models.rule import Rule
from app.schemas.rule import RuleBase, RuleRead

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("/", response_model=List[RuleRead])
def list_rules(scope_type: str = None, db: Session = Depends(get_db)):
    query = db.query(Rule)
    if scope_type:
        query = query.filter(Rule.scope_type == scope_type)
    return query.all()


@router.get("/{rule_id}", response_model=RuleRead)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.post("/", response_model=RuleRead)
def create_rule(data: RuleBase, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    rule = Rule(**data.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.put("/{rule_id}", response_model=RuleRead)
def update_rule(rule_id: int, data: RuleBase, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    for field, value in data.model_dump().items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), _auth: bool = Depends(require_admin)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"detail": "Deleted"}

from pydantic import BaseModel
from typing import Optional


class RuleBase(BaseModel):
    scope_type: str
    scope_id: Optional[int] = None
    condition_type: str
    condition_value: Optional[str] = None
    message: str
    regulation_citation: str
    severity: str = "warning"


class RuleRead(RuleBase):
    id: int

    class Config:
        from_attributes = True

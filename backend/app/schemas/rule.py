from pydantic import BaseModel, ConfigDict
from typing import Optional


class RuleBase(BaseModel):
    scope_type: str
    scope_id: Optional[int] = None
    condition_type: str
    condition_value: Optional[str] = None
    message: str
    regulation_citation: str
    severity: str = "warning"
    source: str = ""


class RuleRead(RuleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

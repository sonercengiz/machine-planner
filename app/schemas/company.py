from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
      "from_attributes": True
    }

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}

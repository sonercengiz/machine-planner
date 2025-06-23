from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from app.schemas.company import CompanyRead


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_superuser: Optional[bool] = False
    company_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    company: Optional[CompanyRead]

    class Config:
        orm_mode = True

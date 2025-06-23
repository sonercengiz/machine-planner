from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.company import CompanyRead


class ModelBase(BaseModel):
    name: str
    is_active: bool = True
    # Firma ID listesi
    company_ids: Optional[List[int]] = []


class ModelCreate(ModelBase):
    # GLB dosyası upload için: FastAPI tarafında UploadFile olarak alınır,
    # Pydantic bunda sadece metadata tutar.
    pass


class ModelUpdate(ModelBase):
    # Tüm alanlar opsiyonel olsun:
    name: Optional[str] = None
    is_active: Optional[bool] = None
    company_ids: Optional[List[int]] = None


class ModelRead(ModelBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
    # İlişkili firma nesneleri
    companies: List[CompanyRead] = []

    model_config = {
      "from_attributes": True
    }

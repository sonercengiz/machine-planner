# app/api/routers/model.py
import os
from typing import List, Optional
from fastapi import (
    APIRouter, Depends, File, UploadFile,
    HTTPException, status, Form, Request
)
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.model import ModelCreate, ModelRead, ModelUpdate
from app.services.auth_service import get_current_active_user
from app.services.model_service import ModelService
from app.db.session import get_db
from app.models.model import Model as ModelModel

router = APIRouter(prefix="/models", tags=["models"])
service = ModelService()

@router.post(
    "/",
    response_model=ModelRead,
    status_code=status.HTTP_201_CREATED,
)
def create_model(
    request: Request,
    name: str = Form(...),
    company_ids: Optional[str] = Form(""),  # virgülle ayrılmış IDs
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Parse company IDs
    ids = [int(i) for i in company_ids.split(",") if i.strip()]
    obj_in = ModelCreate(name=name, company_ids=ids)
    model_obj = service.create(db, obj_in, file)

    # Ensure we only use basename, then build the full URL
    filename = os.path.basename(model_obj.file_path)
    model_obj.file_path = f"{request.base_url}files/{filename}"
    return model_obj

@router.get("/", response_model=List[ModelRead])
def list_models(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    models = service.list_by_user(db, current_user, skip, limit)
    for m in models:
        filename = os.path.basename(m.file_path)
        m.file_path = f"{request.base_url}files/{filename}"
    return models

@router.put("/{model_id}", response_model=ModelRead)
def update_model(
    request: Request,
    model_id: int,
    name: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    company_ids: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    db_obj = db.get(ModelModel, model_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Model not found")

    ids = (
        [int(i) for i in (company_ids or "").split(",") if i.strip()]
        if company_ids is not None
        else None
    )
    obj_in = ModelUpdate(name=name, is_active=is_active, company_ids=ids)
    updated = service.update(db, db_obj, obj_in, file)

    # Again, use basename and full URL
    filename = os.path.basename(updated.file_path)
    updated.file_path = f"{request.base_url}files/{filename}"
    return updated

@router.delete("/{model_id}", response_model=ModelRead)
def delete_model(
    request: Request,
    model_id: int,
    db: Session = Depends(get_db),
):
    obj = service.soft_delete(db, model_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Model not found")

    filename = os.path.basename(obj.file_path)
    obj.file_path = f"{request.base_url}files/{filename}"
    return obj

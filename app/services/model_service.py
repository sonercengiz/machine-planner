from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.user import User
from app.repositories.model_repository import ModelRepository
from app.schemas.model import ModelCreate, ModelUpdate
from app.models.model import Model

_repo = ModelRepository()

class ModelService:
    def create(
        self,
        db: Session,
        obj_in: ModelCreate,
        file: UploadFile
    ) -> Model:
        return _repo.create(db, obj_in=obj_in, file=file)

    def update(
        self,
        db: Session,
        db_obj: Model,
        obj_in: ModelUpdate,
        file: Optional[UploadFile] = None
    ) -> Model:
        return _repo.update(db, db_obj=db_obj, obj_in=obj_in, file=file)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[Model]:
        return _repo.get_multi(db, skip, limit)
    
    def list_by_user(self, db: Session, user: User, skip: int = 0, limit: int = 100):
        if user.is_superuser:
            return _repo.get_multi(db, skip=skip, limit=limit)
        else:
            return _repo.get_by_company(db, user.company_id, skip=skip, limit=limit)

    def soft_delete(self, db: Session, model_id: int) -> Optional[Model]:
        return _repo.soft_delete(db, model_id)

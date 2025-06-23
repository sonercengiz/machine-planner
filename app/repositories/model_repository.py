import os
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from app.models.company import Company
from app.models.model import Model, model_company
from app.schemas.model import ModelCreate, ModelUpdate
from app.core.config import settings
import re
import uuid


class ModelRepository:
    def get(self, db: Session, model_id: int) -> Optional[Model]:
        return db.get(Model, model_id)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Model]:
        return db.query(Model).filter(Model.is_deleted == False).offset(skip).limit(limit).all()
    
    def get_by_company(self, db: Session, company_id: int, skip=0, limit=100):
        return (
            db.query(Model)
            .join(Model.companies)
            .options(selectinload(Model.companies))
            .filter(Model.is_active == True, Model.companies.any(id=company_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self,
        db: Session,
        *,
        obj_in: ModelCreate,
        file: UploadFile
    ) -> Model:
        # Dosya boyutu kontrolü
        upload_dir = settings.MODEL_UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)

        # Güvenli dosya adı: uuid + regex temizleme
        ext = os.path.splitext(file.filename)[1]
        if ext.lower() != ".glb":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sadece .glb uzantılı dosya yüklenebilir."
            )

        unique_name = f"{uuid.uuid4().hex}{ext}"
        safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", unique_name)
        save_path = os.path.join(upload_dir, safe_name)

        # Akışla yazma ve boyut sayma
        size = 0
        with open(save_path, "wb") as buffer:
            for chunk in file.file:
                size += len(chunk)
                if size > settings.MAX_MODEL_FILE_SIZE:
                    buffer.close()
                    os.remove(save_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="Dosya boyutu 200 MB’ı aşıyor."
                    )
                buffer.write(chunk)

        # Model kaydı
        db_obj = Model(
            name=obj_in.name,
            file_path=save_path,
            is_active=obj_in.is_active,
        )
        # İlk ilişkileri kur
        if obj_in.company_ids:
            companies = db.query(model_company.c.company_id).filter(
                model_company.c.company_id.in_(obj_in.company_ids)
            )
            db_obj.companies = db.query(Company).filter(Company.id.in_(obj_in.company_ids)).all()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Model,
        obj_in: ModelUpdate,
        file: Optional[UploadFile] = None
    ) -> Model:
        # (Dosya handling varsa burada…)

        # 1) exclude_unset ile gönderilmeyenleri at, exclude_none ile None'ları da at
        update_data = obj_in.dict(exclude_unset=True, exclude_none=True)

        # 2) company_ids özelinde: boş liste geldiyse at, değilse ilişki set et
        if "company_ids" in update_data:
            new_ids = update_data.pop("company_ids") or []
            if new_ids:
                from app.models.company import Company
                db_obj.companies = (
                    db.query(Company)
                      .filter(Company.id.in_(new_ids))
                      .all()
                )

        # 3) Geri kalan alanları uygula
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, model_id: int) -> Model:
        obj = self.get(db, model_id)
        if obj:
            obj.is_deleted = False
            db.commit()
            db.refresh(obj)
        return obj

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate


class CompanyRepository:
    def get(self, db: Session, company_id: int) -> Optional[Company]:
        return db.get(Company, company_id)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
        return db.query(Company).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        db_obj = Company(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        company_id: int,
        obj_in: "CompanyUpdate",
    ) -> Optional[Company]:
        db_obj = self.get(db, company_id)
        if not db_obj:
            return None
        # exclude_unset & exclude_none ile yalnızca gelenleri al
        update_data = obj_in.dict(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, company_id: int) -> Company:
        obj = self.get(db, company_id)
        if obj:
            obj.is_active = False
            db.commit()
            db.refresh(obj)
        return obj

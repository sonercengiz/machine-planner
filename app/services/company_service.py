from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.models.company import Company

_repo = CompanyRepository()

class CompanyService:
    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        return _repo.create(db, obj_in=obj_in)

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
        return _repo.get_multi(db, skip, limit)
    
    def update(self, db: Session, company_id: int, obj_in: CompanyUpdate) -> Optional[Company]:
        return _repo.update(db, company_id=company_id, obj_in=obj_in)
  
    def soft_delete(self, db: Session, company_id: int) -> Optional[Company]:
        return _repo.soft_delete(db, company_id)

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.company_service import CompanyService
from app.db.session import get_db

router = APIRouter(prefix="/companies", tags=["companies"])
service = CompanyService()

@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(get_db),
):
    return service.create(db, company_in)

@router.get("/", response_model=List[CompanyRead])
def list_companies(
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return service.list(db, skip, limit)

@router.put("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int,
    company_in: CompanyUpdate,
    db: Session = Depends(get_db),
):
    updated = service.update(db, company_id, company_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated

@router.delete("/{company_id}", response_model=CompanyRead)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    obj = service.soft_delete(db, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return obj

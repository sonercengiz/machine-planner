# app/api/routers/user.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate, UserCreate
from app.services.user_service import UserService
from app.services.auth_service import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_current_active_superuser(current_user = Depends(get_current_active_user)):
    """
    Sadece is_superuser=True olan kullanıcıların erişimine izin verir.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return current_user

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (admin only)",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_active_superuser),
):
    """
    Yeni bir kullanıcı oluşturur. Sadece superuser erişebilir.
    Normal kullanıcı için company_id zorunludur.
    """
    user_service = UserService()

    # Eğer superuser değilse company_id zorunlu
    if not user_in.is_superuser and not user_in.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Normal kullanıcı için company_id zorunludur."
        )

    created = user_service.create_user(db, user_in)
    return created


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
)
def read_users_me(
    current_user = Depends(get_current_active_user),
):
    return current_user


@router.get(
    "/",
    response_model=List[UserRead],
    summary="List users (admin only)",
)
def read_users(
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_active_superuser),
    skip: int = 0,
    limit: int = 100,
):
    """
    Tüm kullanıcıları listeler. Sadece superuser erişebilir.
    """
    user_service = UserService()
    return user_service.list_users(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by ID (admin only)",
)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_active_superuser),
):
    """
    ID ile kullanıcı bilgisi döner. Sadece superuser erişebilir.
    """
    user_service = UserService()
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Update user (admin only)",
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_active_superuser),
):
    """
    Kullanıcıyı günceller. Opsiyonel alanlar gönderilebilir.
    Sadece superuser erişebilir.
    """
    user_service = UserService()
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    updated = user_service.update_user(db, user, user_in)
    return updated


@router.delete(
    "/{user_id}",
    response_model=UserRead,
    summary="Delete user (admin only)",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(get_current_active_superuser),
):
    """
    Kullanıcıyı siler. Sadece superuser erişebilir.
    """
    user_service = UserService()
    deleted = user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return deleted

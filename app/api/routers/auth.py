# app/api/routers/auth.py

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserRead
from app.services.auth_service import authenticate_user, create_access_token_for_user
from app.services.user_service import UserService

router = APIRouter()

@router.post(
    "/login/access-token",
    response_model=Token,
    summary="Authenticate and get access token",
)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 şemasıyla kullanıcıyı doğrular (email=form_data.username).
    Başarılıysa JWT access token döner.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = create_access_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}
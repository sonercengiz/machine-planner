from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Şifreleme için bcrypt kullanıyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT konfigürasyon değerleri
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Düz metin parolayı, hashlenmiş haliyle karşılaştırır.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Düz metni bcrypt ile hashler.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Any, expires_delta: Optional[timedelta] = None
) -> str:
    """
    subject (ör. kullanıcı ID'si) bilgisiyle bir JWT oluşturur.
    expires_delta belirtilmezse ayar dosyasındaki değeri kullanır.
    """
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: Dict[str, Any] = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    JWT'yi decode eder, geçerliyse payload'u döner, değilse None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

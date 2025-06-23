# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings

# SQLAlchemy engine (pool_pre_ping ile bağlantı düşmelerine karşı kontrol)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

# Oturum fabrika fonksiyonu
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Generator:
    """
    FastAPI dependency olarak kullanılacak:
      - Her istek başına yeni bir DB oturumu yaratır
      - İstek sonunda kapatır
    Kullanımı:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

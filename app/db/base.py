# app/db/base.py

from sqlalchemy.ext.declarative import declarative_base

# Tüm SQLAlchemy modelleriniz bu Base sınıfından türeyecek.
Base = declarative_base()

from app.models.model import Model
from app.models.company import Company
from app.models.user import User
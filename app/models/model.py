import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base

# Ara tablo (many-to-many)
model_company = Table(
    "model_company",
    Base.metadata,
    Column("model_id", ForeignKey("models.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
)


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    file_path = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # İlişki
    companies = relationship(
        "Company",
        secondary=model_company,
        backref="models",
        passive_deletes=True,
    )

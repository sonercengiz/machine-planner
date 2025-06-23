from typing import List, Optional

from sqlalchemy.orm import Session, selectinload

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        return (
            db.query(User)
            .options(selectinload(User.company))
            .filter(User.id == user_id, User.is_active == True)
            .first()
        )

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.email == email, User.is_active == True)
            .first()
        )

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(User)
            .options(selectinload(User.company))
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self, db: Session, *, obj_in: UserCreate, hashed_password: str
    ) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=hashed_password,
            is_superuser=obj_in.is_superuser or False,
            company_id=obj_in.company_id or None,
            is_active=True  # yeni kullanıcı aktif olarak başlar
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data:
            from app.core.security import get_password_hash
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_remove(self, db: Session, user_id: int) -> Optional[User]:
        db_obj = db.get(User, user_id)
        if db_obj and db_obj.is_active:
            db_obj.is_active = False
            db.commit()
            db.refresh(db_obj)
        return db_obj

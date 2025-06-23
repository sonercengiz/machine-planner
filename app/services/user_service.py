from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

_user_repo = UserRepository()


class UserService:
    def __init__(self, repo: UserRepository = _user_repo):
        self.repo = repo

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        hashed = get_password_hash(user_in.password)
        return self.repo.create(db, obj_in=user_in, hashed_password=hashed)

    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return self.repo.get(db, user_id)

    def list_users(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return self.repo.get_multi(db, skip=skip, limit=limit)

    def update_user(
        self, db: Session, db_obj: User, obj_in: UserUpdate
    ) -> User:
        return self.repo.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete_user(self, db: Session, user_id: int) -> Optional[User]:
        return self.repo.soft_remove(db, user_id)

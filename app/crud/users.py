from typing import Union, Optional, Dict, Any

from sqlalchemy.orm import Session

from app.utils.security import get_hashed_password

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[User]:
        return db.query(User).filter(User.name == name).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            name=obj_in.name,
            hashed_passoword=get_hashed_password(obj_in.password),
            is_admin=obj_in.is_admin
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self,
               db: Session,
               *,
               db_obj: User,
               obj_in: Union[UserUpdate,
                             Dict[str, Any]]
               ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude=True)
        if (password := update_data.get("password") is not None):
            hashed_password = get_hashed_password(password)
            update_data.pop("password")
            update_data.add(hashed_password)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(User)

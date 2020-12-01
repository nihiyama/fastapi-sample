from typing import Union, Optional, Dict, Any

from sqlalchemy.orm import Session

from app.utils.security import verify_password, get_hashed_password

from app.crud.base import CRUDBase
from app.crud.tenants import tenant
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[User]:
        return db.query(User).filter(User.name == name).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            name=obj_in.name,
            hashed_password=get_hashed_password(obj_in.password),
            is_superuser=obj_in.is_superuser,
        )
        if len(t_n_ := obj_in.tenant_names) > 0:
            db_t = tenant.get_by_names(db, tenant_names=t_n_)
            db_obj.tenants = db_t
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
            update_data = obj_in.dict(exclude_unset=True)
        if (password := update_data.get("password")) is not None:
            hashed_password = get_hashed_password(password)
            update_data.pop("password")
            update_data["hashed_password"] = hashed_password
            print(update_data)
        if len(t_n_ := obj_in.tenant_names) > 0:
            db_t = tenant.get_by_names(db, tenant_names=t_n_)
            db_obj.tenants = db_t
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, name: str,
                     password: str) -> Optional[User]:
        user = self.get_by_name(db, name=name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)

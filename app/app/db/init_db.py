from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.config import settings


def init_db(db: Session) -> None:
    user = crud.user.get_by_name(
        db,
        name=settings.FIRST_SUPERUSER,
    )
    if not user:
        user_in = schemas.UserCreate(
            name=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD
        )
        user = crud.user.create(db, obj_in=user_in)

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.utils import security
from app.utils.config import settings

router = APIRouter()


@router.post("/auth/login/access-token")
async def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(
        db,
        name=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "expires_in": access_token_expires
    }

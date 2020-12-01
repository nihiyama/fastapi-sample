from datetime import datetime, timedelta
from typing import Any, Union

from passlib.context import CryptContext
from jose import jwt

from app.utils.config import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encode_jwt


def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

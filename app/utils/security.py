from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

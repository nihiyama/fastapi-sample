import secrets
import os
from typing import (
    List, Union
    # Optional, Any, Dict
)

from pydantic import (
    AnyHttpUrl, BaseSettings, validator
    # HttpUrl,
    # PostgresDsn,
)


class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR", "api/v1")
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    SERVER_NAME: str = os.getenv("SERVER_NAME", "project")
    # SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv(
        "BACKEND_CORS_ORIGINS", '["http://0.0.0.0"]')

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origin(
            cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "fastapi")
    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    SQLALCHEMY_DATABASE_URI: str = \
        rf"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" + \
        f"@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(
    #         cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv(
        "FIRST_SUPERUSER_PASSWORD", "admin")

    class Config:
        case_sensitive = True


settings = Settings()

from typing import Optional, List

from pydantic import BaseModel

from app.schemas.tenant import Tenant


class UserBase(BaseModel):
    name: Optional[str] = None
    is_superuser: bool = False
    tenants: List[Tenant] = []


class UserCreate(UserBase):
    name: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

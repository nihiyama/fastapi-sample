from typing import Optional, List

from pydantic import BaseModel

from app.schemas.tenant import Tenant


class UserBase(BaseModel):
    name: Optional[str] = None
    is_admin: bool = False


class UserCreate(UserBase):
    name: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    tenants: List[Tenant] = []

    class Config:
        orm_mode = True

from typing import Optional, List

from pydantic import BaseModel

from app.schemas.tenant import Tenant


class UserBase(BaseModel):
    name: Optional[str] = None
    is_superuser: bool = False


class UserCreate(UserBase):
    name: str
    password: str
    tenant_names: List[str] = []


class UserUpdate(UserBase):
    password: Optional[str] = None
    tenant_names: List[str] = []


class User(UserBase):
    id: int
    tenants: List[Tenant] = []

    class Config:
        orm_mode = True

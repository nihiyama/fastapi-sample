from typing import Optional

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: Optional[str] = None


class TenantCreate(TenantBase):
    name: str


class TenantUpdate(TenantBase):
    pass


class Tenant(TenantBase):
    id: int

    class Config:
        orm_mode = True

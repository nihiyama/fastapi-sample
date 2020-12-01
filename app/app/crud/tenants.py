from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):

    def get_by_ids(
            self,
            db: Session,
            *,
            tenant_ids: List[int]) -> List[Tenant]:
        return db.query(Tenant).filter(Tenant.id.in_(tenant_ids)).all()

    def get_by_names(
            self,
            db: Session,
            *,
            tenant_names: List[str]) -> List[Tenant]:
        return db.query(Tenant).filter(Tenant.name.in_(tenant_names)).all()


tenant = CRUDTenant(Tenant)

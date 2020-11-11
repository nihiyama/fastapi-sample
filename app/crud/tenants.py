from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):

    def get_by_ids(self, db: Session, *, tenant_ids: int) -> List[Tenant]:
        return db.query(Tenant).filter(Tenant.id.in_(tenant_ids)).all()


tenant = CRUDTenant(Tenant)

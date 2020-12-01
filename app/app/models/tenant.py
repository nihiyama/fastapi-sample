from sqlalchemy import (
    Column, Integer, String,
    DateTime, func
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.user_tenant_map import user_tenant_map_table


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship(
        "User",
        secondary=user_tenant_map_table,
        primaryjoin=(user_tenant_map_table.c.tenant_id == id),
        back_populates="tenants"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now())

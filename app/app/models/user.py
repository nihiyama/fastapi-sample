from sqlalchemy import (
    Boolean, Column, Integer, String,
    DateTime, func
)
from sqlalchemy.orm import relationships

from app.db.database import Base
from app.models.user_tenant_map import user_tenant_map_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)

    tenants = relationships(
        "Tenant",
        secondary=user_tenant_map_table,
        back_populates="users"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now())
    deleted_at = Column(DateTime, server_default=func.now())

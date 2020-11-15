from sqlalchemy import (
    Column, Integer, String,
    DateTime, func
)
from sqlalchemy.orm import relationships

from app.db.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationships("User", back_populates="tenants")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now())
    deleted_at = Column(DateTime, server_default=func.now())

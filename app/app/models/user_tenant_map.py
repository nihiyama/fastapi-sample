from sqlalchemy import (Table, ForeignKey, Column, Integer)

from app.db.database import Base

user_tenant_map_table = Table(
    'user_tenant_map',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('tenant_id', Integer, ForeignKey('tenants.id'))
)

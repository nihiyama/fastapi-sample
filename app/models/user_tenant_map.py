from sqlalchemy import (Table, ForeignKey, Column, Integer)

from app.database import Base

user_tenant_map_table = Table(
    'user_tenant_map',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('tenant_id', Integer, ForeignKey('tenant.id'))
)

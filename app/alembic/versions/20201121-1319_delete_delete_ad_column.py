"""delete delete ad column

Revision ID: c8f8808cc3f8
Revises: df17ec354ac0
Create Date: 2020-11-21 13:19:23.896882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f8808cc3f8'
down_revision = 'df17ec354ac0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'deleted_at')
    op.drop_column('tenants', 'deleted_at')


def downgrade():
    op.add_column(
        'users',
        sa.Column(
            'deleted_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True)
    )
    op.add_column(
        'tenants',
        sa.Column(
            'deleted_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True)
    )

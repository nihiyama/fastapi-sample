"""first create

Revision ID: df17ec354ac0
Revises:
Create Date: 2020-11-15 15:34:54.689103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df17ec354ac0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'tenants',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False),
        sa.Column(
            'name',
            sa.String(),
            nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.Column(
            'deleted_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_tenants_id'), 'tenants', ['id'], unique=False)
    op.create_index(op.f('ix_tenants_name'), 'tenants', ['name'], unique=True)
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False),
        sa.Column(
            'name',
            sa.String(
                length=255),
            nullable=True),
        sa.Column(
            'hashed_password',
            sa.String(
                length=255),
            nullable=False),
        sa.Column(
            'is_superuser',
            sa.Boolean(),
            nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.Column(
            'deleted_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('user_tenant_map',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('tenant_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tenant_map')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tenants_name'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_id'), table_name='tenants')
    op.drop_table('tenants')
    # ### end Alembic commands ###

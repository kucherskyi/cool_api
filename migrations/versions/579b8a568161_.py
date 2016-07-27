"""empty message

Revision ID: 579b8a568161
Revises: test_migr
Create Date: 2016-07-27 16:46:33.422301

"""

# revision identifiers, used by Alembic.
revision = '579b8a568161'
down_revision = 'test_migr'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    ### end Alembic commands ###

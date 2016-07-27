"""created migration for is_admin
Revision ID: test_migr
Revises: fba104753a11
Create Date: 2016-07-27 00:00:00.309885
"""

# revision identifiers, used by Alembic.
revision = 'test_migr'
down_revision = 'fba104753a11'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE users ALTER COLUMN is_admin TYPE boolean USING is_admin::boolean;')


def downgrade():
    op.alter_column('users', 'is_admin', type = sa.Integer())

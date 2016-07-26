revision = ''
down_revision = ''

from alembic import op
import sqlalchemy as sa


def upgrade():
	
	op.execute('ALTER TABLE users ALTER COLUMN is_admin TYPE boolean USING is_admin::boolean;')


def downgrade():
    op.alter_column('users', 'is_admin', type = sa.Integer())

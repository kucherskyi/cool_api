"""update status type

Revision ID: 54334d63c2c8
Revises: 32fcf6a86b91
Create Date: 2016-08-03 18:15:42.110621

"""

# revision identifiers, used by Alembic.
revision = '54334d63c2c8'
down_revision = '32fcf6a86b91'

from alembic import op
import sqlalchemy as sa


status_type = sa.Enum('completed', 'in_progress',
                                  name='task_statuses')

def upgrade():
    status_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE tasks ALTER COLUMN status TYPE task_statuses USING status::task_statuses;')


def downgrade():
    op.execute('ALTER TABLE tasks ALTER COLUMN status TYPE varchar(16) USING status::text;')
    status_type.drop(op.get_bind(), checkfirst=False)

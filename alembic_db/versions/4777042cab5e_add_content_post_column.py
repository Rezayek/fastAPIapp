"""add content post column

Revision ID: 4777042cab5e
Revises: 2a314ee21728
Create Date: 2023-03-03 21:31:43.878119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4777042cab5e'
down_revision = '2a314ee21728'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

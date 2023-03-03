"""create user table

Revision ID: dc72b8462cf2
Revises: fd973a2444dc
Create Date: 2023-03-02 21:21:29.661639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc72b8462cf2'
down_revision = 'fd973a2444dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('email', sa.String, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    
    pass



def downgrade():
    op.drop_table('users')
    pass

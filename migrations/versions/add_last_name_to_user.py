"""
Add last_name to users

Revision ID: add_last_name_to_user
Revises: 710f35a70e2e
Create Date: 2025-09-30
"""

# revision identifiers, used by Alembic.
revision = 'add_last_name_to_user'
down_revision = '5f007c089a82'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'last_name')

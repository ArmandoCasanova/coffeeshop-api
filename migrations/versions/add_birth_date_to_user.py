"""
Add birth_date to users

Revision ID: add_birth_date_to_user
Revises: add_last_name_to_user
Create Date: 2025-09-30
"""

# revision identifiers, used by Alembic.
revision = 'add_birth_date_to_user'
down_revision = 'add_last_name_to_user'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('birth_date', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('users', 'birth_date')

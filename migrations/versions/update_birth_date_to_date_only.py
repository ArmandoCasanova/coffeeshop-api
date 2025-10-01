"""
Add birth_date as date (no time) to users

Revision ID: update_birth_date_to_date_only
Revises: add_birth_date_to_user
Create Date: 2025-09-30
"""

# revision identifiers, used by Alembic.
revision = 'update_birth_date_to_date_only'
down_revision = 'add_birth_date_to_user'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.alter_column('users', 'birth_date', type_=sa.Date(), existing_type=sa.DateTime())

def downgrade():
    op.alter_column('users', 'birth_date', type_=sa.DateTime(), existing_type=sa.Date())

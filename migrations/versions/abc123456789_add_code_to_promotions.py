"""add code field to promotions table

Revision ID: abc123456789
Revises: add_desc_details_001
Create Date: 2025-11-03 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc123456789'
down_revision: Union[str, Sequence[str], None] = 'add_desc_details_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add code column to promotions table."""
    # Add code column as nullable first
    op.add_column('promotions', sa.Column('code', sa.String(length=50), nullable=True))
    
    # Create unique index on code
    op.create_index('ix_promotions_code', 'promotions', ['code'], unique=True)


def downgrade() -> None:
    """Downgrade schema - Remove code column from promotions table."""
    # Drop index first
    op.drop_index('ix_promotions_code', table_name='promotions')
    
    # Drop column
    op.drop_column('promotions', 'code')

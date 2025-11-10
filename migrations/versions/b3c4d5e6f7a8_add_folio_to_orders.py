"""add_folio_to_orders

Revision ID: b3c4d5e6f7a8
Revises: a2b3c4d5e6f7
Create Date: 2025-11-09 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3c4d5e6f7a8'
down_revision: Union[str, Sequence[str], None] = 'a2b3c4d5e6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add folio column to orders table
    op.add_column('orders', sa.Column('folio', sa.String(length=10), nullable=True))
    
    # Create unique index on folio
    op.create_index('idx_orders_folio', 'orders', ['folio'], unique=True)


def downgrade() -> None:
    # Drop index first
    op.drop_index('idx_orders_folio', table_name='orders')
    
    # Drop column
    op.drop_column('orders', 'folio')

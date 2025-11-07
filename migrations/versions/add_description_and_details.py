"""add description to products and details to order_item


Revision ID: add_desc_details_001
Revises: f798db5b99f8
Create Date: 2025-11-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_desc_details_001'
down_revision: Union[str, Sequence[str], None] = 'f798db5b99f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add description column to products and details column to order_item."""
    # Add description to products table
    op.add_column('products', sa.Column('description', sa.String(), nullable=True))
    
    # Add details to order_item table
    op.add_column('order_item', sa.Column('details', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove description from products and details from order_item."""
    # Remove description from products
    op.drop_column('products', 'description')
    
    # Remove details from order_item
    op.drop_column('order_item', 'details')

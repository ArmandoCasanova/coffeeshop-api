"""add_image_url_to_product_categories

Revision ID: f798db5b99f8
Revises: 7998d1010f36
Create Date: 2025-11-02 06:00:19.690377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f798db5b99f8'
down_revision: Union[str, Sequence[str], None] = '7998d1010f36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add image_url column to product_categories table
    op.add_column('product_categories', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove image_url column from product_categories table
    op.drop_column('product_categories', 'image_url')

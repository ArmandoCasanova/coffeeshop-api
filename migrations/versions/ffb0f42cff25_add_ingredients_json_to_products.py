"""add_ingredients_json_to_products

Revision ID: ffb0f42cff25
Revises: abc123456789
Create Date: 2025-11-04 03:29:22.746213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffb0f42cff25'
down_revision: Union[str, Sequence[str], None] = 'abc123456789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('ingredients_json', sa.dialects.postgresql.JSONB(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'ingredients_json')

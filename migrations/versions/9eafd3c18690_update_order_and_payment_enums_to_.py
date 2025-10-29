"""update order and payment enums to english

Revision ID: 9eafd3c18690
Revises: ee9c91070800
Create Date: 2025-10-15 05:24:14.768213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9eafd3c18690'
down_revision: Union[str, Sequence[str], None] = 'ee9c91070800'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.get_bind()  # no-op placeholder to keep Alembic happy


def downgrade() -> None:
    """Downgrade schema."""
    op.get_bind()

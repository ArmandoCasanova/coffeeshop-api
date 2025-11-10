"""merge heads

Revision ID: a9cae6c56e75
Revises: d4adcb818b15, ffb0f42cff25
Create Date: 2025-11-09 01:28:50.630678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9cae6c56e75'
down_revision: Union[str, Sequence[str], None] = ('d4adcb818b15', 'ffb0f42cff25')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

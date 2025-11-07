"""create_stripe_customers

Revision ID: d4adcb818b15
Revises: f798db5b99f8
Create Date: 2025-11-05 02:07:48.478492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4adcb818b15'
down_revision: Union[str, Sequence[str], None] = 'f798db5b99f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stripe_customers',
        sa.Column('id', sa.Uuid(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('customer_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    


def downgrade() -> None:
    op.drop_table('stripe_customers')

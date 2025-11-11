"""add_points_config_and_update_orders

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2025-11-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c4d5e6f7a8b9'
down_revision: Union[str, Sequence[str], None] = 'b3c4d5e6f7a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create points_config table
    op.create_table(
        'points_config',
        sa.Column('config_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('conversion_percentage', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    
    # Add points_used column to orders table
    op.add_column('orders', sa.Column('points_used', sa.Float(), nullable=False, server_default='0.0'))
    
    # Update points_earned to have default value
    op.alter_column('orders', 'points_earned', server_default='0.0')
    
    # Drop points_used table (moving functionality to orders.points_used)
    op.drop_table('points_used')
    
    # Insert default configuration (1% conversion)
    op.execute("""
        INSERT INTO points_config (config_id, conversion_percentage, is_active, created_at, updated_at)
        VALUES (gen_random_uuid(), 1.0, true, now(), now())
    """)


def downgrade() -> None:
    # Recreate points_used table
    op.create_table(
        'points_used',
        sa.Column('points_used_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('orders.order_id')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('points_used', sa.Float()),
    )
    
    # Remove points_used column from orders
    op.drop_column('orders', 'points_used')
    
    # Drop points_config table
    op.drop_table('points_config')

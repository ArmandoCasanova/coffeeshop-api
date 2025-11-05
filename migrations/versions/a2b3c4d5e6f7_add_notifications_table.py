"""add_notifications_table

Revision ID: a2b3c4d5e6f7
Revises: ffb0f42cff25
Create Date: 2025-11-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a2b3c4d5e6f7'
down_revision: Union[str, Sequence[str], None] = 'ffb0f42cff25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notifications',
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True),
        sa.Column('type', sa.String(length=32), nullable=False),
        sa.Column('subtype', sa.String(length=32), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('data', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index('idx_notifications_userid_createdat', 'notifications', ['user_id', 'created_at'])
    op.create_index('idx_notifications_userid_isread', 'notifications', ['user_id', 'is_read'])


def downgrade() -> None:
    op.drop_index('idx_notifications_userid_createdat', table_name='notifications')
    op.drop_index('idx_notifications_userid_isread', table_name='notifications')
    op.drop_table('notifications')

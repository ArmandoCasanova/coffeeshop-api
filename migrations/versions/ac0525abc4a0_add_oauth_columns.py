"""add_oauth_columns

Revision ID: ac0525abc4a0
Revises: c857f2862324
Create Date: 2026-02-23 18:45:08.304944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac0525abc4a0'
down_revision: Union[str, Sequence[str], None] = 'c857f2862324'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""   
    # Agregar columnas OAuth al modelo de usuarios
    op.add_column('users', sa.Column('oauth_provider', sa.String(), nullable=True))
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('oauth_email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('picture_url', sa.String(), nullable=True))
    
    # Crear índices para mayor velocidad de búsqueda
    op.create_index(op.f('ix_users_oauth_provider'), 'users', ['oauth_provider'], unique=False)
    op.create_index(op.f('ix_users_oauth_provider_id'), 'users', ['oauth_provider_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar índices
    op.drop_index(op.f('ix_users_oauth_provider_id'), table_name='users')
    op.drop_index(op.f('ix_users_oauth_provider'), table_name='users')
    
    # Eliminar columnas
    op.drop_column('users', 'picture_url')
    op.drop_column('users', 'oauth_email_verified')
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'oauth_provider')

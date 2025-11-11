"""create_reports_table

Revision ID: c857f2862324
Revises: abc123456789
Create Date: 2025-11-04 05:37:26.486616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c857f2862324'
down_revision: Union[str, Sequence[str], None] = 'abc123456789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### Definición manual de la migración ###
    
    # 1. Crear el tipo ENUM para el estado
    # Usamos sa.Enum para compatibilidad; 'report_status' es el nombre en PostgreSQL
    report_status_enum = sa.Enum(
        'en_proceso', 'generado', 'error', 
        name='reportstatus' # Alembic/SQLAlchemy prefiere nombres en minúsculas para ENUMs
    )
    report_status_enum.create(op.get_bind(), checkfirst=True)

    # 2. Crear la tabla 'reports'
    op.create_table(
        'reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False, index=True),
        sa.Column(
            'status',
            # Usamos el tipo ENUM que acabamos de definir
            sa.Enum('en_proceso', 'generado', 'error', name='reportstatus'),
            nullable=False,
            default='en_proceso',
            index=True
        ),
        sa.Column(
            'request_date',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('file_url', sa.String(length=512), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### Definición manual del downgrade ###
    
    # 1. Eliminar la tabla 'reports'
    op.drop_table('reports')
    
    # 2. Eliminar el tipo ENUM
    report_status_enum = sa.Enum(
        'en_proceso', 'generado', 'error', 
        name='reportstatus'
    )
    report_status_enum.drop(op.get_bind())
    # ### end Alembic commands ###
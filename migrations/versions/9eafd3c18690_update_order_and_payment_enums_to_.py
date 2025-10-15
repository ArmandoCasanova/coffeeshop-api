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
    # Cambiar ENUM OrderStatus
    op.execute("ALTER TYPE orderstatus RENAME TO orderstatus_old;")
    op.execute("CREATE TYPE orderstatus AS ENUM ('pending', 'paid', 'delivered', 'cancelled');")
    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE orderstatus USING \
        CASE status \
            WHEN 'pendiente' THEN 'pending' \
            WHEN 'pagado' THEN 'paid' \
            WHEN 'entregado' THEN 'delivered' \
            WHEN 'cancelado' THEN 'cancelled' \
        END::orderstatus;")
    op.execute("DROP TYPE orderstatus_old;")

    # Cambiar ENUM PaymentType
    op.execute("ALTER TYPE paymenttype RENAME TO paymenttype_old;")
    op.execute("CREATE TYPE paymenttype AS ENUM ('cash', 'card', 'points');")
    op.execute("ALTER TABLE orders ALTER COLUMN payment_type TYPE paymenttype USING \
        CASE payment_type \
            WHEN 'efectivo' THEN 'cash' \
            WHEN 'tarjeta' THEN 'card' \
            WHEN 'puntos' THEN 'points' \
        END::paymenttype;")
    op.execute("DROP TYPE paymenttype_old;")


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir ENUM OrderStatus
    op.execute("ALTER TYPE orderstatus RENAME TO orderstatus_new;")
    op.execute("CREATE TYPE orderstatus AS ENUM ('pendiente', 'pagado', 'entregado', 'cancelado');")
    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE orderstatus USING \
        CASE status \
            WHEN 'pending' THEN 'pendiente' \
            WHEN 'paid' THEN 'pagado' \
            WHEN 'delivered' THEN 'entregado' \
            WHEN 'cancelled' THEN 'cancelado' \
        END::orderstatus;")
    op.execute("DROP TYPE orderstatus_new;")

    # Revertir ENUM PaymentType
    op.execute("ALTER TYPE paymenttype RENAME TO paymenttype_new;")
    op.execute("CREATE TYPE paymenttype AS ENUM ('efectivo', 'tarjeta', 'puntos');")
    op.execute("ALTER TABLE orders ALTER COLUMN payment_type TYPE paymenttype USING \
        CASE payment_type \
            WHEN 'cash' THEN 'efectivo' \
            WHEN 'card' THEN 'tarjeta' \
            WHEN 'points' THEN 'puntos' \
        END::paymenttype;")
    op.execute("DROP TYPE paymenttype_new;")

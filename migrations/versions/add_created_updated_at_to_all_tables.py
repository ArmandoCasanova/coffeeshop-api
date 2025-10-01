"""
Add created_at and updated_at to all tables

Revision ID: add_created_updated_at
Revises: update_birth_date_to_date_only
Create Date: 2025-09-30
"""

# revision identifiers, used by Alembic.
revision = 'add_created_updated_at'
down_revision = 'update_birth_date_to_date_only'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    op.add_column('verification_codes', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('verification_codes', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('verification_codes_password_reset', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
        # Las columnas 'created_at' y 'updated_at' ya existen en 'users', 'user_qr_codes' y 'products'
    op.add_column('promotions', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('orders', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('orders', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_promotions', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_promotions', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('order_item', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('order_item', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('order_item_customization', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('order_item_customization', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_ingredients', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_ingredients', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('customization_options', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('customization_options', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('customization_groups', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('customization_groups', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_customization_groups', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_customization_groups', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('ingredients', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('ingredients', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_categories', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_categories', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_category_link', sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow))
    op.add_column('product_category_link', sa.Column('updated_at', sa.DateTime(), nullable=True, default=datetime.utcnow))

def downgrade():
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('verification_codes', 'created_at')
    op.drop_column('verification_codes', 'updated_at')
    op.drop_column('verification_codes_password_reset', 'created_at')
    op.drop_column('verification_codes_password_reset', 'updated_at')
    op.drop_column('user_qr_codes', 'created_at')
    op.drop_column('user_qr_codes', 'updated_at')
    op.drop_column('points_used', 'created_at')
    # Las columnas 'created_at' y 'updated_at' ya existen en 'users', 'user_qr_codes' y 'products'
    op.drop_column('orders', 'updated_at')
    op.drop_column('product_promotions', 'created_at')
    op.drop_column('product_promotions', 'updated_at')
    op.drop_column('order_item', 'created_at')
    op.drop_column('order_item', 'updated_at')
    op.drop_column('order_item_customization', 'created_at')
    op.drop_column('order_item_customization', 'updated_at')
    op.drop_column('product_ingredients', 'created_at')
    op.drop_column('product_ingredients', 'updated_at')
    op.drop_column('customization_options', 'created_at')
    op.drop_column('customization_options', 'updated_at')
    op.drop_column('customization_groups', 'created_at')
    op.drop_column('customization_groups', 'updated_at')
    op.drop_column('product_customization_groups', 'created_at')
    op.drop_column('product_customization_groups', 'updated_at')
    op.drop_column('ingredients', 'created_at')
    op.drop_column('ingredients', 'updated_at')
    op.drop_column('product_categories', 'created_at')
    op.drop_column('product_categories', 'updated_at')
    op.drop_column('products', 'created_at')
    op.drop_column('products', 'updated_at')
    op.drop_column('product_category_link', 'created_at')
    op.drop_column('product_category_link', 'updated_at')

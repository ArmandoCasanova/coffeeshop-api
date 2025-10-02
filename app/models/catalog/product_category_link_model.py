from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID

class ProductCategoryLinkModel(SQLModel, table=True):
    __tablename__ = "product_category_link"
    product_id: UUID = Field(foreign_key="products.product_id", primary_key=True)
    category_id: UUID = Field(foreign_key="product_categories.category_id", primary_key=True)

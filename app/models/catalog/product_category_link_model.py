from typing import Optional
from sqlmodel import SQLModel, Field

class ProductCategoryLinkModel(SQLModel, table=True):
    __tablename__ = "product_category_link"
    product_id: int = Field(foreign_key="products.product_id", primary_key=True)
    category_id: int = Field(foreign_key="product_categories.category_id", primary_key=True)

from typing import Optional
from sqlmodel import SQLModel, Field

class ProductCategoryModel(SQLModel, table=True):
    __tablename__ = "product_categories"
    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

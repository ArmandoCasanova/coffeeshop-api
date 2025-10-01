from typing import Optional
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel

class ProductCategoryModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "product_categories"
    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

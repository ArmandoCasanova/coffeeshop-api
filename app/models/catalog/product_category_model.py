from typing import Optional
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4

class ProductCategoryModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "product_categories"
    category_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: str

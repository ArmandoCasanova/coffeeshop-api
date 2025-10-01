from typing import Optional
from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID

class ProductIngredientModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "product_ingredients"
    product_id: UUID = Field(foreign_key="products.product_id", primary_key=True)
    ingredient_id: UUID = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
    quantity_required: float

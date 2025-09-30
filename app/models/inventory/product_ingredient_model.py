from typing import Optional
from sqlmodel import SQLModel, Field

class ProductIngredientModel(SQLModel, table=True):
    __tablename__ = "product_ingredients"
    product_id: int = Field(foreign_key="products.product_id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id", primary_key=True)
    quantity_required: float

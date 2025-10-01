from typing import Optional
from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel

class IngredientModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit_of_measure: str
    stock_current_level: int
    stock_optimal_level: int

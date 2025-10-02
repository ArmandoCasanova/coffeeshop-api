from typing import Optional
from sqlmodel import Field
from uuid import UUID, uuid4
from app.core.base_model import BaseCoffeeAppModel

class IngredientModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "ingredients"
    ingredient_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    unit_of_measure: str
    stock_current_level: int
    stock_optimal_level: int

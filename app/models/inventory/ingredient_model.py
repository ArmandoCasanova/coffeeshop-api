from typing import Optional
from sqlmodel import SQLModel, Field

class IngredientModel(SQLModel, table=True):
    __tablename__ = "ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit_of_measure: str
    stock_current_level: int
    stock_optimal_level: int

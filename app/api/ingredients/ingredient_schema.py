from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class IngredientCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    unit_of_measure: str = Field(min_length=1, max_length=20)
    stock_current_level: int = Field(ge=0)
    stock_optimal_level: int = Field(gt=0)


class IngredientUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    unit_of_measure: Optional[str] = Field(None, min_length=1, max_length=20)
    stock_current_level: Optional[int] = Field(None, ge=0)
    stock_optimal_level: Optional[int] = Field(None, gt=0)


class IngredientResponseSchema(BaseModel):
    ingredient_id: UUID
    name: str
    unit_of_measure: str
    stock_current_level: int
    stock_optimal_level: int
    created_at: datetime  # Campo heredado de BaseCoffeeAppModel
    updated_at: datetime  # Campo heredado de BaseCoffeeAppModel

    class Config:
        from_attributes = True


class IngredientListResponseSchema(BaseModel):
    ingredients: List[IngredientResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10


class LowStockIngredientSchema(BaseModel):
    ingredient_id: UUID
    name: str
    stock_current_level: int
    stock_optimal_level: int
    deficit: int  # optimal - current

    class Config:
        from_attributes = True


class IngredientStockUpdateSchema(BaseModel):
    stock_current_level: int = Field(ge=0, description="New stock level")
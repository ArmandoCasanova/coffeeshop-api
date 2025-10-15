from typing import Optional
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4

class CustomizationOptionModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "customization_options"
    option_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    group_id: UUID = Field(foreign_key="customization_groups.group_id")
    name: str
    extra_cost: float
    is_size_option: bool = Field(default=False)
    consumed_ingredient_id: UUID = Field(foreign_key="ingredients.ingredient_id", nullable=True)
    quantity_consumed: float = Field(default=0.0)
    details: str

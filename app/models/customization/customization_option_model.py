from typing import Optional
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel

class CustomizationOptionModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "customization_options"
    option_id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="customization_groups.group_id")
    name: str
    extra_cost: float
    details: str

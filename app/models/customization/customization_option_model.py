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
    details: str

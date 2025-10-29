from typing import Optional
from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4

class CustomizationGroupModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "customization_groups"
    group_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    system_name: str
    display_name: str

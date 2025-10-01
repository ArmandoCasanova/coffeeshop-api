from typing import Optional
from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel

class CustomizationGroupModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "customization_groups"
    group_id: Optional[int] = Field(default=None, primary_key=True)
    name: str

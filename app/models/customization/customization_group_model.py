from typing import Optional
from sqlmodel import SQLModel, Field

class CustomizationGroupModel(SQLModel, table=True):
    __tablename__ = "customization_groups"
    group_id: Optional[int] = Field(default=None, primary_key=True)
    name: str

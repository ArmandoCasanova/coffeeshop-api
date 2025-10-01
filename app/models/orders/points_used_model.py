from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class PointsUsedModel(SQLModel, table=True):
    __tablename__ = "points_used"
    points_used_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    order_id: UUID = Field(foreign_key="orders.order_id")
    user_id: UUID = Field(foreign_key="users.user_id")
    points_used: float

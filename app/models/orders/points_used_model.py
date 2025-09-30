from typing import Optional
from sqlmodel import SQLModel, Field

class PointsUsedModel(SQLModel, table=True):
    __tablename__ = "points_used"
    points_used_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    user_id: int = Field(foreign_key="users.user_id")
    points_used: float

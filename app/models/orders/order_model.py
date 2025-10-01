from typing import Optional
from sqlmodel import Field, Column, Enum
from app.core.base_model import BaseCoffeeAppModel
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum

class OrderStatus(str, enum.Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    entregado = "entregado"
    cancelado = "cancelado"

class OrderModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "orders"
    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: OrderStatus = Field(sa_column=Column(Enum(OrderStatus), nullable=False))
    total_amount: float
    points_earned: float
    items_summary_json: dict = Field(sa_column=Column(JSONB))

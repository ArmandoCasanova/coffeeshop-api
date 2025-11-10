from typing import Optional
from sqlmodel import Field, Column, Enum
from app.core.base_model import BaseCoffeeAppModel
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import UUID, uuid4
import enum

class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    delivered = "delivered"
    cancelled = "cancelled"

class PaymentType(str, enum.Enum):
    cash = "cash"
    card = "card"
    points = "points"

class OrderModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "orders"
    order_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    folio: Optional[str] = Field(default=None, index=True, unique=True, max_length=10)
    user_id: UUID = Field(foreign_key="users.user_id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: OrderStatus = Field(sa_column=Column(Enum(OrderStatus), nullable=False))
    total_amount: float
    points_earned: float = Field(default=0.0)
    points_used: float = Field(default=0.0)
    payment_type: PaymentType = Field(sa_column=Column(Enum(PaymentType), nullable=False))
    items_summary_json: dict = Field(sa_column=Column(JSONB))

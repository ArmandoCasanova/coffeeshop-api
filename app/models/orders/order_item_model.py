from typing import Optional
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4

class OrderItemModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "order_item"
    order_item_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    order_id: UUID = Field(foreign_key="orders.order_id")
    product_id: UUID = Field(foreign_key="products.product_id")
    quantity: int
    price_at_purchase: float

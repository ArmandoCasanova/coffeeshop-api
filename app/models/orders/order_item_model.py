from typing import Optional
from sqlmodel import SQLModel, Field

class OrderItemModel(SQLModel, table=True):
    __tablename__ = "order_item"
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    product_id: int = Field(foreign_key="products.product_id")
    quantity: int
    price_at_purchase: float

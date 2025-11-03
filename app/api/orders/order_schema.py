from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from app.models.orders.order_model import OrderStatus, PaymentType


class UserSimpleSchema(BaseModel):
    user_id: UUID
    name: str
    last_name: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class OrderItemCustomizationCreateSchema(BaseModel):
    option_id: UUID
    option_name: str
    group_name: str
    extra_cost_at_purchase: float

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OrderItemCreateSchema(BaseModel):
    product_id: UUID
    product_name: str
    product_image: str
    quantity: int
    base_price: float
    price_at_purchase: float
    details: Optional[str] = None
    customizations: List[OrderItemCustomizationCreateSchema]

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OrderCreateSchema(BaseModel):
    payment_type: PaymentType
    items: List[OrderItemCreateSchema]

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OrderResponseSchema(BaseModel):
    order_id: UUID
    user: UserSimpleSchema
    order_date: datetime
    status: OrderStatus
    total_amount: float
    payment_type: PaymentType
    items_summary_json: list

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class OrderListResponseSchema(BaseModel):
    total: int
    page: int
    page_size: int
    orders: list[OrderResponseSchema]

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class OrderUpdateStatusSchema(BaseModel):
    status: OrderStatus
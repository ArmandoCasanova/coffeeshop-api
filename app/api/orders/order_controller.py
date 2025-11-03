from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException

from .order_service import OrderService
from .order_schema import (
    OrderCreateSchema,
    OrderUpdateStatusSchema,
)


class OrderController:
    def __init__(self, session: Session):
        self.session = session
        self.service = OrderService(session)

    async def create_order(self, user_id: UUID, order_data: OrderCreateSchema):
        """Create a new order"""
        return await self.service.create_order(user_id, order_data)

    async def get_all_orders(self, page: int, page_size: int, status):
        """Get all orders with pagination"""
        return await self.service.get_all_orders(page, page_size, status)

    async def get_user_orders(self, user_id: UUID, page: int, page_size: int):
        """Get orders for a specific user"""
        return await self.service.get_user_orders(user_id, page, page_size)

    async def get_order_by_id(self, order_id: UUID):
        """Get a specific order"""
        return await self.service.get_order_by_id(order_id)

    async def update_order_status(self, order_id: UUID, data: OrderUpdateStatusSchema):
        """Update order status"""
        return await self.service.update_order_status(order_id, data)

    async def delete_order(self, order_id: UUID):
        """Delete an order"""
        return await self.service.delete_order(order_id)

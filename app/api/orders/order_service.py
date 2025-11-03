from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException
from datetime import datetime

from app.core.http_response import CoffeeAppHttpResponse
from app.models.orders.order_model import OrderModel, OrderStatus, PaymentType
from .order_repository import OrderRepository
from .order_schema import (
    OrderCreateSchema,
    OrderResponseSchema,
    OrderUpdateStatusSchema,
    OrderItemCreateSchema,
)


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = OrderRepository(session)

    async def create_order(self, user_id: UUID, order_data: OrderCreateSchema):
        """Create a new order with items and customizations"""
        try:
            # Calculate total amount from items
            total_amount = sum(
                item.price_at_purchase * item.quantity for item in order_data.items
            )

            # Create items summary for quick reference
            items_summary = [
                {
                    "product_id": str(item.product_id),
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price_at_purchase,
                }
                for item in order_data.items
            ]

            # Calculate points earned (1% of total)
            points_earned = total_amount * 0.01

            # Create order
            order = await self.repository.create_order(
                user_id=user_id,
                total_amount=total_amount,
                points_earned=points_earned,
                payment_type=order_data.payment_type,
                items_summary_json=items_summary,
            )

            # Create order items with customizations
            for item_data in order_data.items:
                await self.repository.create_order_item(
                    order_id=order.order_id,
                    product_id=item_data.product_id,
                    quantity=item_data.quantity,
                    price_at_purchase=item_data.price_at_purchase,
                    details=item_data.details,
                    customizations=item_data.customizations,
                )

            self.session.commit()
            self.session.refresh(order)

            # Get user info
            user = await self.repository.get_user(user_id)
            order_data_dict = order.model_dump()
            order_data_dict["user"] = user

            return OrderResponseSchema.model_validate(order_data_dict)

        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            print(f"Error creating order: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def get_all_orders(
        self, page: int, page_size: int, status: OrderStatus | None
    ):
        """Get all orders with pagination and optional status filter"""
        try:
            orders, total_count = await self.repository.get_all_orders(
                page, page_size, status
            )

            orders_list = []
            for order, user in orders:
                order_data = order.model_dump()
                order_data["user"] = user
                orders_list.append(OrderResponseSchema.model_validate(order_data))

            return {
                "total": total_count,
                "page": page,
                "page_size": page_size,
                "orders": orders_list,
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error getting orders: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def get_user_orders(self, user_id: UUID, page: int, page_size: int):
        """Get orders for a specific user"""
        try:
            orders, total_count = await self.repository.get_user_orders(
                user_id, page, page_size
            )

            orders_list = []
            for order, user in orders:
                order_data = order.model_dump()
                order_data["user"] = user
                orders_list.append(OrderResponseSchema.model_validate(order_data))

            return {
                "total": total_count,
                "page": page,
                "page_size": page_size,
                "orders": orders_list,
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error getting user orders: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def get_order_by_id(self, order_id: UUID):
        """Get a specific order by ID"""
        try:
            order, user = await self.repository.get_order_by_id(order_id)
            if not order:
                CoffeeAppHttpResponse.not_found(message="Order not found")

            order_data = order.model_dump()
            order_data["user"] = user
            return OrderResponseSchema.model_validate(order_data)
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error getting order: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def update_order_status(self, order_id: UUID, data: OrderUpdateStatusSchema):
        """Update order status"""
        try:
            order = await self.repository.update_order_status(order_id, data.status)
            if not order:
                CoffeeAppHttpResponse.not_found(message="Order not found")

            self.session.commit()
            self.session.refresh(order)

            user = await self.repository.get_user(order.user_id)
            order_data = order.model_dump()
            order_data["user"] = user
            return OrderResponseSchema.model_validate(order_data)
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            print(f"Error updating order status: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def delete_order(self, order_id: UUID) -> dict:
        """Delete an order and all its items"""
        try:
            success = await self.repository.delete_order(order_id)
            if not success:
                CoffeeAppHttpResponse.not_found(message="Order not found")

            self.session.commit()
            return {"message": "Order deleted successfully"}
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting order: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

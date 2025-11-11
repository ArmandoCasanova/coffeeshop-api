from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException
from datetime import datetime
import random
import string

from app.core.http_response import CoffeeAppHttpResponse
from app.models.orders.order_model import OrderModel, OrderStatus, PaymentType
from .order_repository import OrderRepository
from .order_schema import (
    OrderCreateSchema,
    OrderResponseSchema,
    OrderUpdateStatusSchema,
    OrderUpdatePaymentTypeSchema,
    OrderItemCreateSchema,
)


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = OrderRepository(session)

    def _generate_folio(self) -> str:
        """Generate a unique 8-character folio (e.g., CF240A3B)"""
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=6))
        return f"CF{random_part}"

    async def _ensure_unique_folio(self) -> str:
        """Generate a folio and ensure it's unique"""
        max_attempts = 10
        for _ in range(max_attempts):
            folio = self._generate_folio()
            existing = await self.repository.get_order_by_folio(folio)
            if not existing:
                return folio
        timestamp = datetime.now().strftime("%H%M%S")
        return f"CF{timestamp}"

    async def create_order(self, user_id: UUID, order_data: OrderCreateSchema):
        """Create a new order with items and customizations"""
        try:

            from app.api.points.points_service import PointsService
            points_service = PointsService(self.session)
            
            folio = await self._ensure_unique_folio()
            
            total_amount = sum(
                item.price_at_purchase * item.quantity for item in order_data.items
            )

            promotion_discount = 0
            if order_data.promotion:
                # Calcular el descuento según el tipo de promoción
                if order_data.promotion.discount_type == "percentage":
                    # Descuento por porcentaje
                    promotion_discount = total_amount * (order_data.promotion.discount_value / 100)
                elif order_data.promotion.discount_type == "fixed_amount":
                    # Descuento de monto fijo
                    promotion_discount = order_data.promotion.discount_value
                
                # Aplicar el descuento al total
                total_amount -= promotion_discount

            total_amount = max(0, total_amount)

            user = await self.repository.get_user(user_id)
            
            points_used = order_data.points_used or 0.0
            if points_used > 0:
                if points_used > user.points:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No tienes suficientes puntos. Disponibles: {user.points}"
                    )
                
                # Deduct points from total (1 punto = 1 peso)
                points_discount = min(points_used, total_amount)
                total_amount -= points_discount
                points_used = points_discount
                
                # If paid entirely with points, set payment_type to points
                if total_amount == 0:
                    order_data.payment_type = PaymentType.points
            
            # Calculate points earned (only if not paid entirely with points)
            if order_data.payment_type == PaymentType.points:
                points_earned = 0.0  # No points earned when paying with points
            else:
                # Calculate based on original amount before points discount
                original_amount = total_amount + points_used
                points_earned = await points_service.calculate_points_earned(original_amount)

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

            # Add promotion info to summary if provided
            if order_data.promotion:
                items_summary.append({
                    "promotion": {
                        "promotion_id": str(order_data.promotion.promotion_id),
                        "code": order_data.promotion.code,
                        "discount_type": order_data.promotion.discount_type,
                        "discount_value": order_data.promotion.discount_value,
                        "discount_applied": promotion_discount,  # El descuento calculado
                    }
                })

            # Create order
            order = await self.repository.create_order(
                user_id=user_id,
                folio=folio,
                total_amount=total_amount,
                points_earned=points_earned,
                points_used=points_used,
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

            # Get user info for response
            order_data_dict = order.model_dump()
            order_data_dict["user"] = user

            return OrderResponseSchema.model_validate(order_data_dict)

        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
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
            CoffeeAppHttpResponse.internal_error()

    async def update_order_payment_type(self, order_id: UUID, data: OrderUpdatePaymentTypeSchema):
        """Update order payment type"""
        try:
            order = await self.repository.update_order_payment_type(order_id, data.payment_type)
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
            CoffeeAppHttpResponse.internal_error()

    async def confirm_payment(self, order_id: UUID, user_id: UUID) -> dict:
        """
        Confirm payment: deduct stock, update user points, send notification.
        For orders paid entirely with points, skip payment gateway.
        """
        try:
            result = await self.repository.get_order_by_id(order_id)
            if not result:
                CoffeeAppHttpResponse.not_found(message="Order not found")
            
            order, user = result
            
            if str(order.user_id) != str(user_id):
                raise HTTPException(status_code=403, detail="Access denied: not your order")
            
            if order.status != OrderStatus.pending:
                raise HTTPException(
                    status_code=400,
                    detail=f"Order cannot be paid. Current status: {order.status}"
                )
            
            # Deduct inventory
            from app.services.inventory_service import InventoryService
            inventory_service = InventoryService(self.session)
            
            items_for_stock = []
            if order.items_summary_json:
                for item in order.items_summary_json:
                    items_for_stock.append({
                        "product_id": item.get("product_id"),
                        "quantity": item.get("quantity", item.get("qty")),
                        "customizations": item.get("customizations", {})
                    })
            
            stock_result = await inventory_service.deduct_stock_for_order(items_for_stock)
            
            # Update user points: deduct used points, add earned points
            if order.points_used > 0:
                user.points -= order.points_used
            
            if order.points_earned > 0:
                user.points += order.points_earned
            
            self.session.add(user)
            
            # Update order status
            order.status = OrderStatus.paid
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            self.session.refresh(user)
            
            # Send notifications
            try:
                from app.api.notifications.notification_service import NotificationService
                notification_service = NotificationService(self.session)
                
                # Payment successful notification
                await notification_service.create_notification_safe(
                    user_id=user_id,
                    notification_type="payment_successful",
                    title="¡Compra exitosa!",
                    body=f"Orden {order.folio} confirmada. Total: ${order.total_amount:.2f} MXN.",
                    data={
                        "order_id": str(order.order_id),
                        "folio": order.folio,
                        "total_amount": order.total_amount,
                        "points_earned": order.points_earned,
                        "points_used": order.points_used,
                    }
                )
                
                # Points earned notification (only if earned points)
                if order.points_earned > 0:
                    await notification_service.create_notification_safe(
                        user_id=user_id,
                        notification_type="points",
                        title="¡Puntos recibidos!",
                        body=f"Ganaste {order.points_earned:.0f} puntos en tu compra. Total acumulado: {user.points:.0f} puntos.",
                        data={
                            "points_earned": order.points_earned,
                            "total_points": user.points,
                            "order_id": str(order.order_id),
                            "folio": order.folio,
                        }
                    )
            except Exception:
                pass
            
            from app.api.orders.order_schema import UserSimpleSchema
            
            order_dict = {
                "order_id": order.order_id,
                "folio": order.folio,
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "last_name": user.last_name
                },
                "order_date": order.order_date,
                "status": order.status,
                "total_amount": order.total_amount,
                "payment_type": order.payment_type,
                "items_summary_json": order.items_summary_json
            }
            
            order_response = OrderResponseSchema.model_validate(order_dict)
            
            return {
                "success": True,
                "message": "Payment confirmed successfully",
                "order": order_response,
                "inventory_deduction": stock_result
            }
            
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

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
            CoffeeAppHttpResponse.internal_error()

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
        # Format: CF + 6 random alphanumeric characters
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=6))
        return f"CF{random_part}"

    async def _ensure_unique_folio(self) -> str:
        """Generate a folio and ensure it's unique"""
        max_attempts = 10
        for _ in range(max_attempts):
            folio = self._generate_folio()
            # Check if folio exists
            existing = await self.repository.get_order_by_folio(folio)
            if not existing:
                return folio
        # Fallback: use timestamp-based folio
        timestamp = datetime.now().strftime("%H%M%S")
        return f"CF{timestamp}"

    async def create_order(self, user_id: UUID, order_data: OrderCreateSchema):
        """Create a new order with items and customizations"""
        try:
            # Generate unique folio
            folio = await self._ensure_unique_folio()

            # Calculate total amount from items
            total_amount = sum(
                item.price_at_purchase * item.quantity for item in order_data.items
            )

            # Apply promotion discount if provided
            promotion_discount = 0
            if order_data.promotion:
                promotion_discount = order_data.promotion.discount
                total_amount -= promotion_discount

            # Ensure total is not negative
            total_amount = max(0, total_amount)

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
                        "discount": order_data.promotion.discount,
                    }
                })

            # Calculate points earned (1% of total)
            points_earned = total_amount * 0.01

            # Create order
            order = await self.repository.create_order(
                user_id=user_id,
                folio=folio,
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
            print(f"Error updating order payment type: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def confirm_payment(self, order_id: UUID, user_id: UUID) -> dict:
        """
        Simula confirmación de pago exitoso.
        Cambia status a 'paid' y descuenta stock de ingredientes.
        Envía notificación de compra exitosa (sin bloquear el flujo).
        """
        try:
            print(f"[CONFIRM_PAYMENT] Starting payment confirmation for order_id={order_id}, user_id={user_id}")
            
            # Obtener la orden - el repositorio devuelve (OrderModel, UserModel)
            result = await self.repository.get_order_by_id(order_id)
            if not result:
                CoffeeAppHttpResponse.not_found(message="Order not found")
            
            # Desempaquetar la tupla
            order, user = result
            
            print(f"[CONFIRM_PAYMENT] Order found: order.user_id={order.user_id}, order.status={order.status}")
            
            # Verificar que la orden pertenece al usuario
            if str(order.user_id) != str(user_id):
                raise HTTPException(status_code=403, detail="Access denied: not your order")
            
            # Verificar que la orden está en estado pending
            if order.status != OrderStatus.pending:
                raise HTTPException(
                    status_code=400,
                    detail=f"Order cannot be paid. Current status: {order.status}"
                )
            
            # Importar el servicio de inventario
            from app.services.inventory_service import InventoryService
            inventory_service = InventoryService(self.session)
            
            # Preparar items para descuento de stock
            items_for_stock = []
            if order.items_summary_json:
                print(f"[CONFIRM_PAYMENT] items_summary_json: {order.items_summary_json}")
                for item in order.items_summary_json:
                    print(f"[CONFIRM_PAYMENT] Processing item: {item}")
                    items_for_stock.append({
                        "product_id": item.get("product_id"),
                        "quantity": item.get("quantity", item.get("qty")),
                        "customizations": item.get("customizations", {})
                    })
            
            print(f"[CONFIRM_PAYMENT] items_for_stock prepared: {items_for_stock}")
            
            # Descontar stock de ingredientes
            stock_result = await inventory_service.deduct_stock_for_order(items_for_stock)
            
            # Actualizar status de la orden a 'paid'
            order.status = OrderStatus.paid
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            
            print(f"[CONFIRM_PAYMENT] Payment confirmed successfully, order status updated to 'paid'")
            
            # ========== CRITICAL: Send notification AFTER payment success ==========
            # This runs in a separate try-except to prevent notification errors from breaking the payment
            try:
                from app.api.notifications.notification_service import NotificationService
                notification_service = NotificationService(self.session)
                
                # Create success notification with folio and total
                await notification_service.create_notification_safe(
                    user_id=user_id,
                    notification_type="payment_successful",
                    title="¡Compra exitosa!",
                    body=f"Orden {order.folio} confirmada. Total: ${order.total_amount:.2f} MXN. ¡Ganaste {order.points_earned:.0f} puntos!",
                    data={
                        "order_id": str(order.order_id),
                        "folio": order.folio,
                        "total_amount": order.total_amount,
                        "points_earned": order.points_earned,
                    }
                )
                print(f"[CONFIRM_PAYMENT] Notification sent successfully")
            except Exception as notif_error:
                # Log notification error but DO NOT fail the payment
                print(f"[CONFIRM_PAYMENT] WARNING: Failed to send notification: {str(notif_error)}")
                import traceback
                print(f"[CONFIRM_PAYMENT] Notification error traceback:\n{traceback.format_exc()}")
            # ========================================================================
            
            # Ya tenemos el usuario de la tupla inicial
            print(f"[CONFIRM_PAYMENT] User details: user_id={user.user_id}, name={user.name}, last_name={user.last_name}")
            
            # Preparar datos para el schema de respuesta usando from_attributes
            from app.api.orders.order_schema import UserSimpleSchema
            print(f"[CONFIRM_PAYMENT] Creating UserSimpleSchema from user model")
            
            # Crear un dict temporal que combine order y user
            # El schema tiene from_attributes=True, así que podemos pasar el modelo directamente
            print(f"[CONFIRM_PAYMENT] Creating order dict with user")
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
            
            print(f"[CONFIRM_PAYMENT] Validating OrderResponseSchema")
            order_response = OrderResponseSchema.model_validate(order_dict)
            print(f"[CONFIRM_PAYMENT] OrderResponseSchema validated successfully")
            
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
            print(f"[CONFIRM_PAYMENT] ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"[CONFIRM_PAYMENT] TRACEBACK:\n{traceback.format_exc()}")
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
            print(f"Error deleting order: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

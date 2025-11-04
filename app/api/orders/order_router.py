from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from uuid import UUID
from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user
from app.api.orders.order_controller import OrderController
from app.api.orders.order_schema import (
    OrderCreateSchema,
    OrderListResponseSchema,
    OrderUpdateStatusSchema,
    OrderUpdatePaymentTypeSchema,
    OrderResponseSchema,
)
from app.models.orders.order_model import OrderStatus
from app.models.users.user_model import UserModel

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponseSchema)
async def create_order(
    order_data: OrderCreateSchema,
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new order for the current user"""
    controller = OrderController(session)
    try:
        return await controller.create_order(current_user.user_id, order_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=OrderListResponseSchema)
async def get_all_orders(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    status: OrderStatus | None = Query(None, description="Filtrar por estatus"),
    session: Session = Depends(get_db),
):
    """Get all orders (admin endpoint)"""
    controller = OrderController(session)
    return await controller.get_all_orders(page, page_size, status)


@router.get("/me", response_model=OrderListResponseSchema)
async def get_my_orders(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get orders for the current user"""
    controller = OrderController(session)
    return await controller.get_user_orders(current_user.user_id, page, page_size)


@router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(
    order_id: UUID,
    session: Session = Depends(get_db),
):
    """Get a specific order by ID"""
    controller = OrderController(session)
    try:
        return await controller.get_order_by_id(order_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderResponseSchema)
async def update_order_status(
    order_id: UUID,
    status_data: OrderUpdateStatusSchema,
    session: Session = Depends(get_db),
):
    """Update order status (admin endpoint)"""
    controller = OrderController(session)
    try:
        return await controller.update_order_status(order_id, status_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/payment-type", response_model=OrderResponseSchema)
async def update_order_payment_type(
    order_id: UUID,
    payment_data: OrderUpdatePaymentTypeSchema,
    session: Session = Depends(get_db),
):
    """Update order payment type"""
    controller = OrderController(session)
    try:
        return await controller.update_order_payment_type(order_id, payment_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}")
async def delete_order(order_id: UUID, session: Session = Depends(get_db)):
    """Delete an order (admin endpoint)"""
    controller = OrderController(session)
    try:
        return await controller.delete_order(order_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

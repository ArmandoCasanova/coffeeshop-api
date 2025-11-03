from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from uuid import UUID
from app.core.database import get_db
from app.api.orders.order_controller import OrderController
from app.api.orders.order_schema import (
    OrderListResponseSchema,
    OrderUpdateStatusSchema,
    OrderResponseSchema,
)
from app.models.orders.order_model import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=OrderListResponseSchema)
async def get_all_orders(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    status: OrderStatus | None = Query(None, description="Filtrar por estatus"),
    session: Session = Depends(get_db),
):
    controller = OrderController(session)
    return await controller.get_all_orders(page, page_size, status)


@router.patch("/{order_id}/status", response_model=OrderResponseSchema)
async def update_order_status(
    order_id: UUID,
    status_data: OrderUpdateStatusSchema,
    session: Session = Depends(get_db),
):
    controller = OrderController(session)
    try:
        return await controller.update_order_status(order_id, status_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}")
async def delete_order(order_id: UUID, session: Session = Depends(get_db)):
    controller = OrderController(session)
    try:
        return await controller.delete_order(order_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

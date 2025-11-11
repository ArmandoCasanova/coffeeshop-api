from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.api.promotions.promotion_controller import PromotionController
from app.api.promotions.promotion_schmena import (
    PromotionCreateSchema,
    PromotionUpdateSchema,
    PromotionResponseSchema,
    PromotionListResponseSchema,
)

router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.post("/", response_model=PromotionResponseSchema, status_code=201)
async def create_promotion(
    promotion_data: PromotionCreateSchema, session: Session = Depends(get_db)
):
    controller = PromotionController(session)
    return await controller.create_promotion(promotion_data)


@router.get("/", response_model=PromotionListResponseSchema)
async def get_all_promotions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    session: Session = Depends(get_db),
):
    controller = PromotionController(session)
    return await controller.get_all_promotions(page, page_size, is_active)


@router.get("/{promotion_id}", response_model=PromotionResponseSchema)
async def get_promotion(promotion_id: UUID, session: Session = Depends(get_db)):
    controller = PromotionController(session)
    return await controller.get_promotion(promotion_id)


@router.put("/{promotion_id}", response_model=PromotionResponseSchema)
async def update_promotion(
    promotion_id: UUID,
    promotion_data: PromotionUpdateSchema,
    session: Session = Depends(get_db),
):
    controller = PromotionController(session)
    return await controller.update_promotion(promotion_id, promotion_data)


@router.delete("/{promotion_id}")
async def delete_promotion(promotion_id: UUID, session: Session = Depends(get_db)):
    controller = PromotionController(session)
    return await controller.delete_promotion(promotion_id)


@router.post("/validate", response_model=dict)
async def validate_promotion_code(
    code_data: dict, session: Session = Depends(get_db)
):
    """
    Valida un código de promoción.
    Por ahora valida por nombre de promoción (ya que no hay campo 'code' en la DB).
    """
    controller = PromotionController(session)
    return await controller.validate_promotion_code(code_data.get("code", ""))
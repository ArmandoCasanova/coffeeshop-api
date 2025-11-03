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
    # --- CAMBIO ---
    ProductPromotionListResponseSchema, # Usamos el nuevo esquema de lista
)

router = APIRouter(prefix="/promotions", tags=["Promotions"])


# --- POST, GET (by_id), PUT, DELETE no cambian ---
# Siguen sirviendo para gestionar promociones individuales

@router.post("/", response_model=PromotionResponseSchema, status_code=201)
async def create_promotion(
    promotion_data: PromotionCreateSchema, session: Session = Depends(get_db)
):
    controller = PromotionController(session)
    return await controller.create_promotion(promotion_data)


# --- CAMBIO EN GET / ---
@router.get("/", response_model=ProductPromotionListResponseSchema) # Nuevo response_model
async def get_all_applied_promotions( # Renombrado para claridad
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    # El filtro 'is_active' se elimina, ya que 'estatus' ahora es un campo
    session: Session = Depends(get_db),
):
    controller = PromotionController(session)
    return await controller.get_all_applied_promotions(page, page_size)


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
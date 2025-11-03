from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.promotions.promotion_schmena import (
    PromotionCreateSchema,
    PromotionUpdateSchema,
)
from app.api.promotions.promotion_repository import PromotionRepository
from app.models.promotions.promotion_model import PromotionModel


class PromotionService:
    def __init__(self, session: Session):
        self.promotion_repository = PromotionRepository(session)

    async def create_promotion(self, promotion_data: PromotionCreateSchema) -> object:
        try:
            promotion_dict = promotion_data.model_dump()
            return await self.promotion_repository.create_promotion(promotion_dict)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_promotion_by_id(self, promotion_id: UUID) -> Optional[PromotionModel]:
        try:
            return await self.promotion_repository.get_promotion_by_id(promotion_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_all_promotions(
        self, skip: int = 0, limit: int = 10, is_active: Optional[bool] = None
    ) -> tuple[list, int]:
        try:
            return await self.promotion_repository.get_all_promotions(
                skip, limit, is_active
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_promotion(
        self, promotion_id: UUID, promotion_data: PromotionUpdateSchema
    ) -> Optional[object]:
        try:
            update_data = promotion_data.model_dump(exclude_unset=True)
            return await self.promotion_repository.update_promotion(
                promotion_id, update_data
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def delete_promotion(self, promotion_id: UUID) -> bool:
        try:
            return await self.promotion_repository.delete_promotion(promotion_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
            
    async def get_all_applied_promotions(
        self, skip: int = 0, limit: int = 10
    ) -> tuple[list, int]:
        try:
            return await self.promotion_repository.get_all_applied_promotions(
                skip, limit
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
import logging

# Importamos el servicio y esquemas de promoción
from app.api.promotions.promotion_service import PromotionService
from app.api.promotions.promotion_schmena import (
    ProductPromotionDetailSchema,
    ProductPromotionListResponseSchema,
    PromotionCreateSchema,
    PromotionUpdateSchema,
    PromotionResponseSchema,
    PromotionListResponseSchema,
)

logger = logging.getLogger(__name__)

class PromotionController:
    def __init__(self, session: Session):
        self.session = session
        self.service = PromotionService(session)  

    async def create_promotion(
        self, promotion_data: PromotionCreateSchema
    ) -> PromotionResponseSchema:
        try:
            promotion = await self.service.create_promotion(promotion_data)
            return PromotionResponseSchema.model_validate(promotion)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_promotion(self, promotion_id: UUID) -> PromotionResponseSchema:
        try:
            promotion = await self.service.get_promotion_by_id(promotion_id)
            if not promotion:
                CoffeeAppHttpResponse.not_found(message="Promotion not found")

            return PromotionResponseSchema.model_validate(promotion)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_all_applied_promotions(
        self, page: int = 1, page_size: int = 10
    ) -> ProductPromotionListResponseSchema:
        try:
            skip = (page - 1) * page_size
            applied_promotions, total = await self.service.get_all_applied_promotions(
                skip, page_size
            )
            promotion_list = [
                ProductPromotionDetailSchema.model_validate(promo) 
                for promo in applied_promotions
            ]
            return ProductPromotionListResponseSchema(
                promotions=promotion_list, total=total, page=page, page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            CoffeeAppHttpResponse.internal_error()

    async def update_promotion(
        self, promotion_id: UUID, promotion_data: PromotionUpdateSchema
    ) -> PromotionResponseSchema:
        try:
            promotion = await self.service.update_promotion(promotion_id, promotion_data)
            if not promotion:
                CoffeeAppHttpResponse.not_found(message="Promotion not found")

            return PromotionResponseSchema.model_validate(promotion)
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            CoffeeAppHttpResponse.internal_error()

    async def delete_promotion(self, promotion_id: UUID) -> dict:
        try:
            deleted = await self.service.delete_promotion(promotion_id)
            if not deleted:
                CoffeeAppHttpResponse.not_found(message="Promotion not found")

            return {"message": "Promotion deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            CoffeeAppHttpResponse.internal_error()
    
    async def validate_promotion_code(self, code: str) -> dict:
        try:
            promotion = await self.service.validate_promotion_by_code(code)
            if not promotion:
                return {
                    "valid": False,
                    "message": "Código de promoción no válido o expirado"
                }
            
            promotion_schema = PromotionResponseSchema.model_validate(promotion)
            return {
                "valid": True,
                "promotion": promotion_schema.model_dump(mode='json', by_alias=True)
            }
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            CoffeeAppHttpResponse.internal_error()
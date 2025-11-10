from sqlmodel import Session
from uuid import UUID
from fastapi import HTTPException

from app.api.points.points_service import PointsService
from app.api.points.points_schema import (
    PointsConfigCreateSchema,
    PointsConfigUpdateSchema,
    PointsConfigResponseSchema,
)
from app.core.http_response import CoffeeAppHttpResponse


class PointsController:
    def __init__(self, session: Session):
        self.service = PointsService(session)
    
    async def get_active_config(self):
        """Get active points configuration"""
        try:
            config = await self.service.get_active_config()
            if isinstance(config, dict):
                return config
            return PointsConfigResponseSchema.model_validate(config.model_dump())
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def get_all_configs(self):
        """Get all configurations"""
        try:
            configs = await self.service.get_all_configs()
            return [PointsConfigResponseSchema.model_validate(c.model_dump()) for c in configs]
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def create_config(self, data: PointsConfigCreateSchema):
        """Create new points configuration"""
        try:
            config = await self.service.create_config(data.conversion_percentage)
            return PointsConfigResponseSchema.model_validate(config.model_dump())
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def update_config(self, config_id: UUID, data: PointsConfigUpdateSchema):
        """Update points configuration"""
        try:
            config = await self.service.update_config(
                config_id,
                data.conversion_percentage,
                data.is_active
            )
            return PointsConfigResponseSchema.model_validate(config.model_dump())
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

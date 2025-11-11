from sqlmodel import Session
from uuid import UUID
from typing import Optional
from fastapi import HTTPException

from app.api.points.points_repository import PointsRepository
from app.core.http_response import CoffeeAppHttpResponse


class PointsService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = PointsRepository(session)
    
    async def get_active_config(self):
        """Get active points configuration"""
        try:
            config = await self.repository.get_active_config()
            if not config:
                return {"conversion_percentage": 1.0, "is_active": True}
            return config
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def get_all_configs(self):
        """Get all configurations"""
        try:
            return await self.repository.get_all_configs()
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def create_config(self, conversion_percentage: float):
        """Create new points configuration"""
        try:
            config = await self.repository.create_config(conversion_percentage)
            self.session.commit()
            self.session.refresh(config)
            return config
        except HTTPException:
            self.session.rollback()
            raise
        except Exception:
            self.session.rollback()
            CoffeeAppHttpResponse.internal_error()
    
    async def update_config(self, config_id: UUID, conversion_percentage: Optional[float] = None, is_active: Optional[bool] = None):
        """Update points configuration"""
        try:
            config = await self.repository.update_config(config_id, conversion_percentage, is_active)
            if not config:
                CoffeeAppHttpResponse.not_found(message="Configuration not found")
            
            self.session.commit()
            self.session.refresh(config)
            return config
        except HTTPException:
            self.session.rollback()
            raise
        except Exception:
            self.session.rollback()
            CoffeeAppHttpResponse.internal_error()
    
    async def calculate_points_earned(self, total_amount: float) -> float:
        """Calculate points earned based on total amount and active configuration"""
        config = await self.get_active_config()
        if isinstance(config, dict):
            conversion_percentage = config.get("conversion_percentage", 1.0)
        else:
            conversion_percentage = config.conversion_percentage
        
        points = (total_amount * conversion_percentage) / 100
        return round(points, 2)

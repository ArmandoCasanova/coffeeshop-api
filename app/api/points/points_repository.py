from sqlmodel import Session, select
from uuid import UUID
from typing import Optional
from app.models.points.points_config_model import PointsConfigModel


class PointsRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def get_active_config(self) -> Optional[PointsConfigModel]:
        """Get the active points configuration"""
        statement = select(PointsConfigModel).where(PointsConfigModel.is_active == True).limit(1)
        result = self.session.exec(statement).first()
        return result
    
    async def get_config_by_id(self, config_id: UUID) -> Optional[PointsConfigModel]:
        """Get configuration by ID"""
        return self.session.get(PointsConfigModel, config_id)
    
    async def get_all_configs(self) -> list[PointsConfigModel]:
        """Get all configurations"""
        statement = select(PointsConfigModel).order_by(PointsConfigModel.created_at.desc())
        result = self.session.exec(statement).all()
        return list(result)
    
    async def create_config(self, conversion_percentage: float) -> PointsConfigModel:
        """Create new points configuration"""
        # Deactivate all existing configs
        statement = select(PointsConfigModel).where(PointsConfigModel.is_active == True)
        active_configs = self.session.exec(statement).all()
        for config in active_configs:
            config.is_active = False
            self.session.add(config)
        
        new_config = PointsConfigModel(
            conversion_percentage=conversion_percentage,
            is_active=True
        )
        self.session.add(new_config)
        self.session.flush()
        return new_config
    
    async def update_config(self, config_id: UUID, conversion_percentage: Optional[float] = None, is_active: Optional[bool] = None) -> Optional[PointsConfigModel]:
        """Update points configuration"""
        config = self.session.get(PointsConfigModel, config_id)
        if not config:
            return None
        
        if conversion_percentage is not None:
            config.conversion_percentage = conversion_percentage
        
        if is_active is not None:
            if is_active:
                # Deactivate other configs
                statement = select(PointsConfigModel).where(PointsConfigModel.is_active == True)
                active_configs = self.session.exec(statement).all()
                for active_config in active_configs:
                    if active_config.config_id != config_id:
                        active_config.is_active = False
                        self.session.add(active_config)
            
            config.is_active = is_active
        
        self.session.add(config)
        self.session.flush()
        return config

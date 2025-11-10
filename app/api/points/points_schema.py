from pydantic import BaseModel
from pydantic.alias_generators import to_camel
from uuid import UUID
from typing import Optional


class PointsConfigCreateSchema(BaseModel):
    conversion_percentage: float  # Porcentaje de conversión (1.0 = 1%)
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class PointsConfigUpdateSchema(BaseModel):
    conversion_percentage: Optional[float] = None
    is_active: Optional[bool] = None
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class PointsConfigResponseSchema(BaseModel):
    config_id: UUID
    conversion_percentage: float
    is_active: bool
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

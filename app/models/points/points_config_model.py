from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4


class PointsConfigModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "points_config"
    
    config_id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversion_percentage: float = Field(default=1.0)  # Porcentaje de conversión (ej: 1.0 = 1%, 10.0 = 10%)
    is_active: bool = Field(default=True)

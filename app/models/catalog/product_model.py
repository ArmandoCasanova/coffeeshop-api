
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID, uuid4
from app.core.base_model import BaseCoffeeAppModel

class ProductModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "products"
    product_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: Optional[str] = Field(default=None, nullable=True)
    base_price: float
    image_url: str
    is_available: bool = Field(default=True)
    category_info_json: dict = Field(sa_column=Column(JSONB))
    customization_details_json: dict = Field(sa_column=Column(JSONB))
    ingredients_json: Optional[dict] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

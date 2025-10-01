from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from app.core.base_model import BaseCoffeeAppModel
from datetime import datetime

class ProductModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "products"
    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    base_price: float
    image_url: str
    is_available: bool = Field(default=True)
    category_info_json: dict = Field(sa_column=Column(JSONB))
    customization_details_json: dict = Field(sa_column=Column(JSONB))
    updated_at: datetime = Field(default_factory=datetime.utcnow)

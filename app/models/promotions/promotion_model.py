from typing import Optional
from sqlmodel import Field, Column, Enum
from app.core.base_model import BaseCoffeeAppModel
from datetime import datetime
from uuid import UUID, uuid4
import enum

class DiscountType(str, enum.Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"

class PromotionModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "promotions"
    promotion_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    code: Optional[str] = Field(default=None, max_length=50, index=True, unique=True)
    discount_type: DiscountType = Field(sa_column=Column(Enum(DiscountType), nullable=False))
    discount_value: float
    start_date: datetime
    end_date: datetime

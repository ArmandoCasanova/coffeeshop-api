from typing import Optional
from sqlmodel import SQLModel, Field, Column, Enum
from datetime import datetime
import enum

class DiscountType(str, enum.Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"

class PromotionModel(SQLModel, table=True):
    __tablename__ = "promotions"
    promotion_id: Optional[int] = Field(default=None, primary_key=True)
    discount_type: DiscountType = Field(sa_column=Column(Enum(DiscountType), nullable=False))
    discount_value: float
    start_date: datetime
    end_date: datetime

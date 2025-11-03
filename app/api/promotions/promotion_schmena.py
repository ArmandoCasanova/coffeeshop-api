from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, computed_field
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from enum import Enum
import math

from app.models.promotions.promotion_model import DiscountType

    
class PromotionStatus(str, Enum):
    ACTIVE = "Activa"
    SCHEDULED = "Programada"
    EXPIRED = "Expirada"

class PromotionCreateSchema(BaseModel):
    code: str = Field(min_length=1, max_length=50) 
    discount_type: DiscountType
    discount_value: Decimal = Field(gt=0)
    start_date: datetime
    end_date: datetime

class PromotionUpdateSchema(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50) 
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = Field(None, gt=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class PromotionResponseSchema(BaseModel):
    promotion_id: UUID = Field(alias="promotionId")
    code: Optional[str] = None
    discount_type: DiscountType = Field(alias="discountType")
    discount_value: Decimal = Field(alias="discountValue")
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True

class PromotionListResponseSchema(BaseModel):
    promotions: List[PromotionResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10


class AppliedPromotionResponseSchema(BaseModel):
    product_id: UUID
    promotion_id: UUID
    
    promotion_name: str     
    base_price: Decimal     
    discount_type: DiscountType
    discount_value: Decimal 
    final_price: Decimal    
    duration: str           
    status: str             

class AppliedPromotionListResponseSchema(BaseModel):
    applied_promotions: List[AppliedPromotionResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10
    
class ProductPromotionDetailSchema(BaseModel):
    product_id: UUID
    promotion_id: UUID
    precio: Decimal = Field(..., alias="base_price") 
    discount_type: DiscountType
    discount_value: Decimal
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
        populate_by_name = True 

    @computed_field
    @property
    def precio_final(self) -> Decimal:
        if self.discount_type == DiscountType.fixed_amount:
            final = self.precio - self.discount_value
        elif self.discount_type == DiscountType.percentage:
            discount_amount = (self.precio * self.discount_value) / 100
            final = self.precio - discount_amount
        else:
            final = self.precio
        return max(Decimal("0.00"), final.quantize(Decimal("0.01")))

    @computed_field
    @property
    def duracion(self) -> str:
        delta = self.end_date - self.start_date
        total_days = delta.days
        
        if total_days < 0:
            return "Fechas inválidas"
        if total_days == 0:
            return "Menos de 1 día"
        if total_days == 1:
            return "1 día"
        return f"{total_days} días"

    @computed_field
    @property
    def estatus(self) -> PromotionStatus:
        now = datetime.utcnow()
        if self.start_date > now:
            return PromotionStatus.SCHEDULED
        elif self.end_date < now:
            return PromotionStatus.EXPIRED
        else:
            return PromotionStatus.ACTIVE

class ProductPromotionListResponseSchema(BaseModel):
    promotions: List[ProductPromotionDetailSchema]
    total: int
    page: int = 1
    page_size: int = 10
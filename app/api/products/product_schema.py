from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from uuid import UUID


class ProductCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    base_price: Decimal = Field(gt=0)
    image_url: str
    is_available: bool = True
    category_info_json: Dict[str, Any] = Field(default_factory=dict)
    customization_details_json: Dict[str, Any] = Field(default_factory=dict)


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    base_price: Optional[Decimal] = Field(None, gt=0)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    category_info_json: Optional[Dict[str, Any]] = None
    customization_details_json: Optional[Dict[str, Any]] = None


class ProductResponseSchema(BaseModel):
    product_id: UUID
    name: str
    description: Optional[str] = None
    base_price: Decimal
    image_url: str
    is_available: bool
    category_info_json: Dict[str, Any]
    customization_details_json: Dict[str, Any]
    created_at: datetime  
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True


class ProductListResponseSchema(BaseModel):
    products: List[ProductResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10


class CategoryResponseSchema(BaseModel):
    """Schema for category response including popularity metrics"""

    category_id: str
    name: str
    description: str
    image_url: Optional[str] = None
    total_sales: int = Field(ge=0, description="Total sales/orders for this category")

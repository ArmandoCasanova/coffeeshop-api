from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CategoryCreateSchema(BaseModel):
    """Esquema para crear una nueva categoría."""
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    image_url: Optional[str] = None
    # additional_data_json ELIMINADO


class CategoryUpdateSchema(BaseModel):
    """Esquema para actualizar una categoría existente."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    image_url: Optional[str] = None
    # additional_data_json ELIMINADO


class CategoryResponseSchema(BaseModel):
    """Esquema de respuesta para una categoría. (Coincide con el Modelo)"""
    category_id: UUID
    name: str
    description: str
    image_url: Optional[str] = None
    
    # CAMPOS RESTAURADOS (Existen en el Modelo)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryListResponseSchema(BaseModel):
    """Esquema de respuesta para una lista paginada de categorías."""
    categories: List[CategoryResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10

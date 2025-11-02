from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.api.products.product_controller import ProductController
from app.api.products.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
    ProductListResponseSchema
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponseSchema, status_code=201)
async def create_product(
    product_data: ProductCreateSchema,
    session: Session = Depends(get_db)
):
    """Crear un nuevo producto"""
    controller = ProductController(session)
    return await controller.create_product(product_data)


@router.get("/", response_model=ProductListResponseSchema)
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    is_available: Optional[bool] = Query(None, description="Filter by availability"),
    session: Session = Depends(get_db)
):
    """Obtener todos los productos con paginación y filtros"""
    controller = ProductController(session)
    return await controller.get_all_products(page, page_size, is_available)


@router.get("/search", response_model=ProductListResponseSchema)
async def search_products(
    name: str = Query(..., min_length=1, description="Product name to search"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    session: Session = Depends(get_db)
):
    """Buscar productos por nombre"""
    controller = ProductController(session)
    return await controller.search_products(name, page, page_size)


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: UUID,
    session: Session = Depends(get_db)
):
    """Obtener un producto por ID"""
    controller = ProductController(session)
    return await controller.get_product(product_id)


@router.put("/{product_id}", response_model=ProductResponseSchema)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdateSchema,
    session: Session = Depends(get_db)
):
    """Actualizar un producto"""
    controller = ProductController(session)
    return await controller.update_product(product_id, product_data)


@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    session: Session = Depends(get_db)
):
    """Eliminar un producto"""
    controller = ProductController(session)
    return await controller.delete_product(product_id)


@router.get("/popular/list", response_model=list[ProductResponseSchema])
async def get_popular_products(
    limit: int = Query(10, ge=1, le=50, description="Number of popular products to return"),
    session: Session = Depends(get_db)
):
    """Obtener productos populares basados en ventas de los últimos 7 días"""
    controller = ProductController(session)
    return await controller.get_popular_products(limit)


@router.get("/favorites/user/{user_id}", response_model=list[ProductResponseSchema])
async def get_user_favorite_products(
    user_id: UUID,
    limit: int = Query(10, ge=1, le=50, description="Number of favorite products to return"),
    session: Session = Depends(get_db)
):
    """Obtener productos favoritos de un usuario específico"""
    controller = ProductController(session)
    return await controller.get_user_favorite_products(user_id, limit)
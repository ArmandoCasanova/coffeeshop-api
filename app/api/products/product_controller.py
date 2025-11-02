from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID

from app.api.products.product_service import ProductService
from app.api.products.product_schema import (
    ProductCreateSchema, 
    ProductUpdateSchema, 
    ProductResponseSchema,
    ProductListResponseSchema
)


class ProductController:
    def __init__(self, session: Session):
        self.session = session
        self.service = ProductService(session)

    async def create_product(self, product_data: ProductCreateSchema) -> ProductResponseSchema:
        """Crear un nuevo producto"""
        try:
            product = await self.service.create_product(product_data)
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_product(self, product_id: UUID) -> ProductResponseSchema:
        """Obtener un producto por ID"""
        try:
            product = await self.service.get_product_by_id(product_id)
            if not product:
                    CoffeeAppHttpResponse.not_found(message="Product not found")
            
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_all_products(
        self, 
        page: int = 1, 
        page_size: int = 10,
        is_available: Optional[bool] = None
    ) -> ProductListResponseSchema:
        """Obtener todos los productos con paginación"""
        try:
            skip = (page - 1) * page_size
            products, total = await self.service.get_all_products(skip, page_size, is_available)
            
            product_list = [ProductResponseSchema.model_validate(product) for product in products]
            
            return ProductListResponseSchema(
                products=product_list,
                total=total,
                page=page,
                page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def update_product(
        self, 
        product_id: UUID, 
        product_data: ProductUpdateSchema
    ) -> ProductResponseSchema:
        """Actualizar un producto"""
        try:
            product = await self.service.update_product(product_id, product_data)
            if not product:
                    CoffeeAppHttpResponse.not_found(message="Product not found")
            
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def delete_product(self, product_id: UUID) -> dict:
        """Eliminar un producto"""
        try:
            deleted = await self.service.delete_product(product_id)
            if not deleted:
                    CoffeeAppHttpResponse.not_found(message="Product not found")
            
            return {"message": "Product deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def search_products(
        self, 
        name: str, 
        page: int = 1, 
        page_size: int = 10
    ) -> ProductListResponseSchema:
        """Buscar productos por nombre"""
        try:
            skip = (page - 1) * page_size
            products, total = await self.service.search_products_by_name(name, skip, page_size)
            
            product_list = [ProductResponseSchema.model_validate(product) for product in products]
            
            return ProductListResponseSchema(
                products=product_list,
                total=total,
                page=page,
                page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_popular_products(self, limit: int = 10) -> ProductListResponseSchema:
        """Obtener productos populares basados en ventas"""
        try:
            products = await self.service.get_popular_products(limit=limit)
            product_list = [ProductResponseSchema.model_validate(product) for product in products]
            
            return ProductListResponseSchema(
                products=product_list,
                total=len(product_list),
                page=1,
                page_size=limit
            )
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_user_favorite_products(self, user_id: UUID, limit: int = 10) -> ProductListResponseSchema:
        """Obtener productos favoritos de un usuario"""
        try:
            products = await self.service.get_user_favorite_products(user_id=user_id, limit=limit)
            product_list = [ProductResponseSchema.model_validate(product) for product in products]
            
            return ProductListResponseSchema(
                products=product_list,
                total=len(product_list),
                page=1,
                page_size=limit
            )
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()
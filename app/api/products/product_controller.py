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

    async def create_product(self, product_data: ProductCreateSchema) -> ProductResponseSchema:
        """Crear un nuevo producto"""
        try:
            product = await ProductService.create_product(product_data, self.session)
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_product(self, product_id: UUID) -> ProductResponseSchema:
        """Obtener un producto por ID"""
        try:
            product = await ProductService.get_product_by_id(product_id, self.session)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_products(
        self, 
        page: int = 1, 
        page_size: int = 10,
        is_available: Optional[bool] = None
    ) -> ProductListResponseSchema:
        """Obtener todos los productos con paginación"""
        try:
            skip = (page - 1) * page_size
            products, total = await ProductService.get_all_products(
                self.session, skip, page_size, is_available
            )
            
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
            raise HTTPException(status_code=500, detail=str(e))

    async def update_product(
        self, 
        product_id: UUID, 
        product_data: ProductUpdateSchema
    ) -> ProductResponseSchema:
        """Actualizar un producto"""
        try:
            product = await ProductService.update_product(product_id, product_data, self.session)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return ProductResponseSchema.model_validate(product)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_product(self, product_id: UUID) -> dict:
        """Eliminar un producto"""
        try:
            deleted = await ProductService.delete_product(product_id, self.session)
            if not deleted:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return {"message": "Product deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_products(
        self, 
        name: str, 
        page: int = 1, 
        page_size: int = 10
    ) -> ProductListResponseSchema:
        """Buscar productos por nombre"""
        try:
            skip = (page - 1) * page_size
            products, total = await ProductService.search_products_by_name(
                name, self.session, skip, page_size
            )
            
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
            raise HTTPException(status_code=500, detail=str(e))
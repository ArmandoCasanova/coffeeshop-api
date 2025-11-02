from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.products.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.api.products.product_repository import ProductRepository

class ProductService:
    def __init__(self, session: Session):
        self.product_repository = ProductRepository(session)

    async def create_product(self, product_data: ProductCreateSchema) -> object:
        try:
            product_dict = product_data.model_dump()
            return await self.product_repository.create_product(product_dict)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

    async def get_product_by_id(self, product_id: UUID) -> Optional[object]:
        try:
            return await self.product_repository.get_product_by_id(product_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

    async def get_all_products(self, skip: int = 0, limit: int = 10, is_available: Optional[bool] = None) -> tuple[list, int]:
        try:
            return await self.product_repository.get_all_products(skip, limit, is_available)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

    async def update_product(self, product_id: UUID, product_data: ProductUpdateSchema) -> Optional[object]:
        try:
            update_data = product_data.model_dump(exclude_unset=True)
            return await self.product_repository.update_product(product_id, update_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            return await self.product_repository.delete_product(product_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

    async def search_products_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            return await self.product_repository.search_products_by_name(name, skip, limit)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")
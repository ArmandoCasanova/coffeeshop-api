from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.products.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.api.products.product_repository import ProductRepository
from app.core.redis_client import RedisClient
from app.models.catalog.product_model import ProductModel

# Cache keys and TTL
POPULAR_PRODUCTS_CACHE_KEY = "products:popular"
USER_FAVORITES_CACHE_PREFIX = "user:favorites:"
CACHE_TTL = 3600  # 1 hour

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
            CoffeeAppHttpResponse.internal_error()

    async def get_product_by_id(self, product_id: UUID) -> Optional[object]:
        try:
            return await self.product_repository.get_product_by_id(product_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_all_products(self, skip: int = 0, limit: int = 10, is_available: Optional[bool] = None) -> tuple[list, int]:
        try:
            return await self.product_repository.get_all_products(skip, limit, is_available)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_product(self, product_id: UUID, product_data: ProductUpdateSchema) -> Optional[object]:
        try:
            update_data = product_data.model_dump(exclude_unset=True)
            return await self.product_repository.update_product(product_id, update_data)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            return await self.product_repository.delete_product(product_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def search_products_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            return await self.product_repository.search_products_by_name(name, skip, limit)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_popular_products(self, limit: int = 10) -> List[ProductModel]:
        """Get popular products based on sales from last 7 days with Redis caching"""
        try:
            # Try cache first
            cached_data = await RedisClient.get_json(POPULAR_PRODUCTS_CACHE_KEY)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    # Get products by IDs maintaining order
                    products = await self.product_repository.get_products_by_ids(product_ids, is_available=True)
                    # Maintain order from cache
                    products_dict = {str(p.product_id): p for p in products}
                    ordered_products = [products_dict[pid] for pid in product_ids if pid in products_dict]
                    return ordered_products[:limit]
            
            # Get from database
            products = await self.product_repository.get_popular_products(limit=limit, days=7)
            
            # Cache result
            if products:
                product_ids = [str(p.product_id) for p in products]
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(POPULAR_PRODUCTS_CACHE_KEY, cache_data, ex=CACHE_TTL)
            
            return products
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_user_favorite_products(self, user_id: UUID, limit: int = 10) -> List[ProductModel]:
        """Get user's favorite products with Redis caching"""
        try:
            # Try cache first
            cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
            cached_data = await RedisClient.get_json(cache_key)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    products = await self.product_repository.get_products_by_ids(product_ids, is_available=True)
                    return products[:limit]
            
            # Get from database
            products = await self.product_repository.get_user_favorite_products(user_id=user_id, limit=limit)
            
            # Cache result
            if products:
                product_ids = [str(p.product_id) for p in products]
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(cache_key, cache_data, ex=CACHE_TTL)
            
            return products
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
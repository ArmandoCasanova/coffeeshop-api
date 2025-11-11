from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.products.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.api.products.product_repository import ProductRepository
from app.core.redis_client import RedisClient
from app.models.catalog.product_model import ProductModel

POPULAR_PRODUCTS_CACHE_KEY = "products:popular"
POPULAR_CATEGORIES_CACHE_KEY = "categories:popular"
USER_FAVORITES_CACHE_PREFIX = "user:favorites:"
CACHE_TTL = 3600  


class ProductService:
    def __init__(self, session: Session):
        self.product_repository = ProductRepository(session)

    async def create_product(self, product_data: ProductCreateSchema) -> object:
        try:
            product_dict = product_data.model_dump()
            
            if 'ingredients' in product_dict:
                product_dict['ingredients'] = [
                    {
                        'ingredient_id': ing['ingredient_id'],
                        'quantity_required': ing['quantity_required']
                    }
                    for ing in product_dict['ingredients']
                ]
            
            result = await self.product_repository.create_product(product_dict)
            
            # Invalidar caché de admin products
            await RedisClient.delete("admin:products:all:available=None")
            await RedisClient.delete("admin:products:all:available=True")
            await RedisClient.delete("admin:products:all:available=False")
            
            return result
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

    async def get_all_products(
        self, skip: int = 0, limit: int = 10, is_available: Optional[bool] = None
    ) -> tuple[list, int]:
        try:
            # Crear clave de caché basada en los filtros
            cache_key = f"admin:products:all:available={is_available}"
            
            # Intentar obtener del caché
            cached_data = await RedisClient.get(cache_key)
            if cached_data:
                import json
                data = json.loads(cached_data)
                # Aplicar paginación en memoria
                total = data['total']
                products = data['products'][skip:skip+limit]
                return products, total
            
            # Si no está en caché, consultar DB
            products, total = await self.product_repository.get_all_products(
                skip=0, limit=1000, is_available=is_available  # Obtener más para cachear
            )
            
            # Serializar productos para caché
            products_list = [
                {
                    'product_id': str(p.product_id),
                    'name': p.name,
                    'description': p.description,
                    'base_price': p.base_price,
                    'is_available': p.is_available,
                    'category_id': str(p.category_id) if p.category_id else None,
                    'image_url': p.image_url,
                    'created_at': p.created_at.isoformat() if p.created_at else None,
                    'updated_at': p.updated_at.isoformat() if p.updated_at else None,
                } for p in products
            ]
            
            # Guardar en caché por 3 minutos (180 segundos)
            import json
            await RedisClient.set(
                cache_key, 
                json.dumps({'products': products_list, 'total': total}), 
                ex=180
            )
            
            # Retornar página solicitada
            return products[skip:skip+limit], total
            
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_product(
        self, product_id: UUID, product_data: ProductUpdateSchema
    ) -> Optional[object]:
        try:
            update_data = product_data.model_dump(exclude_unset=True)
            
            if 'ingredients' in update_data and update_data['ingredients'] is not None:
                update_data['ingredients'] = [
                    {
                        'ingredient_id': ing['ingredient_id'],
                        'quantity_required': ing['quantity_required']
                    }
                    for ing in update_data['ingredients']
                ]
            
            result = await self.product_repository.update_product(product_id, update_data)
            
            # Invalidar caché de admin products
            await RedisClient.delete("admin:products:all:available=None")
            await RedisClient.delete("admin:products:all:available=True")
            await RedisClient.delete("admin:products:all:available=False")
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            result = await self.product_repository.delete_product(product_id)
            
            # Invalidar caché de admin products
            await RedisClient.delete("admin:products:all:available=None")
            await RedisClient.delete("admin:products:all:available=True")
            await RedisClient.delete("admin:products:all:available=False")
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def search_products_by_name(
        self, name: str, skip: int = 0, limit: int = 10
    ) -> tuple[list, int]:
        try:
            return await self.product_repository.search_products_by_name(
                name, skip, limit
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_popular_products(self, limit: int = 10) -> List[ProductModel]:
        """Get popular products based on sales from last 7 days with Redis caching"""
        try:
            cached_data = await RedisClient.get_json(POPULAR_PRODUCTS_CACHE_KEY)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    products = self.product_repository.get_products_by_ids(
                        product_ids, is_available=True
                    )
                    products_dict = {str(p.product_id): p for p in products}
                    ordered_products = [
                        products_dict[pid]
                        for pid in product_ids
                        if pid in products_dict
                    ]
                    return ordered_products[:limit]

            products = self.product_repository.get_popular_products(limit=limit, days=7)


            if products:
                product_ids = [str(p.product_id) for p in products]
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(
                    POPULAR_PRODUCTS_CACHE_KEY, cache_data, ex=CACHE_TTL
                )

            return products
        except HTTPException:
            raise
        except Exception as e:
            import traceback

            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

    async def get_user_favorite_products(
        self, user_id: UUID, limit: int = 10
    ) -> List[ProductModel]:
        """Get user's favorite products with Redis caching"""
        try:
            cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
            cached_data = await RedisClient.get_json(cache_key)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    products = self.product_repository.get_products_by_ids(
                        product_ids, is_available=True
                    )
                    return products[:limit]

            products = self.product_repository.get_user_favorite_products(
                user_id=user_id, limit=limit
            )

            if products:
                product_ids = [str(p.product_id) for p in products]
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(cache_key, cache_data, ex=CACHE_TTL)

            return products
        except HTTPException:
            raise
        except Exception as e:
            import traceback

            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

    async def get_popular_categories(self, limit: int = 10) -> List[dict]:
        """Get popular categories based on sales from last 7 days with Redis caching"""
        try:
            cached_data = await RedisClient.get_json(POPULAR_CATEGORIES_CACHE_KEY)
            if cached_data:
                categories = cached_data.get("categories", [])
                if categories:
                    return categories[:limit]

            categories = self.product_repository.get_popular_categories(
                limit=limit, days=7
            )

            if categories:
                cache_data = {"categories": categories}
                await RedisClient.set_json(
                    POPULAR_CATEGORIES_CACHE_KEY, cache_data, ex=CACHE_TTL
                )

            return categories
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error in get_popular_categories: {str(e)}")
            import traceback

            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

    async def check_is_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            # Intentar obtener del caché de Redis primero
            cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
            
            # Verificar si el set de favoritos del usuario existe en caché
            cached_favorites = await RedisClient.get(cache_key)
            
            if cached_favorites is not None:
                # Si existe en caché, verificar si product_id está en el set
                import json
                favorites_set = set(json.loads(cached_favorites))
                return str(product_id) in favorites_set
            
            # Si no está en caché, cargar todos los favoritos del usuario
            all_favorites = await self.product_repository.get_user_favorites(user_id)
            favorites_ids = [str(fav.product_id) for fav in all_favorites]
            
            # Guardar en caché por 15 minutos (900 segundos)
            import json
            await RedisClient.set(cache_key, json.dumps(favorites_ids), ex=900)
            
            # Verificar si el producto está en favoritos
            return str(product_id) in favorites_ids
            
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

    async def add_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            product = await self.product_repository.get_product_by_id(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            result = await self.product_repository.add_favorite(user_id, product_id)
            
            if result:
                cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
                await RedisClient.delete(cache_key)
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

    async def remove_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            result = await self.product_repository.remove_favorite(user_id, product_id)
            
            if result:
                cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
                await RedisClient.delete(cache_key)
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            CoffeeAppHttpResponse.internal_error()

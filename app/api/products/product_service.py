from typing import Optional, List
from sqlmodel import Session, select, func
from fastapi import HTTPException
from uuid import UUID
from datetime import datetime, timedelta

from app.models.catalog.product_model import ProductModel
from app.models.orders.order_item_model import OrderItemModel
from app.models.orders.order_model import OrderModel
from app.models.users.user_favorite_model import UserFavoriteModel
from app.api.products.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.core.redis_client import RedisClient


PRODUCTS_CACHE_KEY = "products:all"
POPULAR_PRODUCTS_CACHE_KEY = "products:popular"
PRODUCT_CACHE_PREFIX = "product:"
USER_FAVORITES_CACHE_PREFIX = "user:favorites:"
CACHE_TTL = 3600  # 1 hora


class ProductService:
    @staticmethod
    async def create_product(product_data: ProductCreateSchema, session: Session) -> ProductModel:
        """Crear un nuevo producto"""
        try:
            product_dict = product_data.model_dump()
            new_product = ProductModel(**product_dict)
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            
            # Invalidate cache
            await RedisClient.delete(PRODUCTS_CACHE_KEY)
            
            return new_product
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

    @staticmethod
    async def get_product_by_id(product_id: UUID, session: Session) -> Optional[ProductModel]:
        """Obtener producto por ID"""
        try:
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = session.exec(statement).first()
            return product
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

    @staticmethod
    async def get_all_products(
        session: Session, 
        skip: int = 0, 
        limit: int = 10,
        is_available: Optional[bool] = None
    ) -> tuple[List[ProductModel], int]:
        """Obtener todos los productos con paginación y caché"""
        try:
            # Try to get from cache first (only for available products without pagination)
            if is_available is True and skip == 0 and limit >= 100:
                cached_data = await RedisClient.get_json(PRODUCTS_CACHE_KEY)
                if cached_data:
                    products_data = cached_data.get("products", [])
                    total = cached_data.get("total", 0)
                    # Convert dict back to ProductModel instances
                    products = [ProductModel.model_validate(p) for p in products_data]
                    return products[:limit], total
            
            # Base query
            query = select(ProductModel)
            # Filter by availability if specified
            if is_available is not None:
                query = query.where(ProductModel.is_available == is_available)
            # Count total
            count_query = select(func.count(ProductModel.product_id))
            if is_available is not None:
                count_query = count_query.where(ProductModel.is_available == is_available)
            total = session.exec(count_query).one()
            # Get paginated results
            query = query.offset(skip).limit(limit).order_by(ProductModel.name)
            products = session.exec(query).all()
            
            # Cache the results for available products
            if is_available is True and skip == 0:
                cache_data = {
                    "products": [p.model_dump() for p in products],
                    "total": total
                }
                await RedisClient.set_json(PRODUCTS_CACHE_KEY, cache_data, ex=CACHE_TTL)
            
            return products, total
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

    @staticmethod
    async def update_product(
        product_id: UUID, 
        product_data: ProductUpdateSchema, 
        session: Session
    ) -> Optional[ProductModel]:
        """Actualizar un producto"""
        try:
            # Get existing product
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = session.exec(statement).first()
            if not product:
                return None
            # Update fields
            update_data = product_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)
            # updated_at se actualiza automáticamente por BaseCoffeeAppModel
            session.add(product)
            session.commit()
            session.refresh(product)
            
            # Invalidate cache
            await RedisClient.delete(PRODUCTS_CACHE_KEY)
            await RedisClient.delete(f"{PRODUCT_CACHE_PREFIX}{product_id}")
            
            return product
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

    @staticmethod
    async def delete_product(product_id: UUID, session: Session) -> bool:
        """Eliminar un producto"""
        try:
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = session.exec(statement).first()
            if not product:
                return False
            session.delete(product)
            session.commit()
            
            # Invalidate cache
            await RedisClient.delete(PRODUCTS_CACHE_KEY)
            await RedisClient.delete(f"{PRODUCT_CACHE_PREFIX}{product_id}")
            
            return True
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

    @staticmethod
    async def search_products_by_name(
        name: str, 
        session: Session, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[ProductModel], int]:
        """Buscar productos por nombre"""
        try:
            # Search query (case insensitive)
            search_pattern = f"%{name}%"
            query = select(ProductModel).where(ProductModel.name.ilike(search_pattern))
            # Count total
            count_query = select(func.count(ProductModel.product_id)).where(
                ProductModel.name.ilike(search_pattern)
            )
            total = session.exec(count_query).one()
            # Get paginated results
            query = query.offset(skip).limit(limit).order_by(ProductModel.name)
            products = session.exec(query).all()
            return products, total
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")

    @staticmethod
    async def get_popular_products(
        session: Session,
        limit: int = 10
    ) -> List[ProductModel]:
        """Obtener productos populares basados en ventas de los últimos 7 días"""
        try:
            # Try to get from cache first
            cached_data = await RedisClient.get_json(POPULAR_PRODUCTS_CACHE_KEY)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    query = select(ProductModel).where(
                        ProductModel.product_id.in_(product_ids),
                        ProductModel.is_available == True
                    )
                    products = session.exec(query).all()
                    # Mantener el orden de popularidad
                    products_dict = {str(p.product_id): p for p in products}
                    return [products_dict[pid] for pid in product_ids if pid in products_dict]
            
            # Calculate from orders of last 7 days
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            
            # Query to get most sold products in last 7 days
            query = (
                select(
                    OrderItemModel.product_id,
                    func.sum(OrderItemModel.quantity).label("total_sold")
                )
                .join(OrderModel, OrderModel.order_id == OrderItemModel.order_id)
                .where(OrderModel.created_at >= seven_days_ago)
                .group_by(OrderItemModel.product_id)
                .order_by(func.sum(OrderItemModel.quantity).desc())
                .limit(limit)
            )
            
            results = session.exec(query).all()
            product_ids = [str(result[0]) for result in results]
            
            # Get product details
            if product_ids:
                products_query = select(ProductModel).where(
                    ProductModel.product_id.in_(product_ids),
                    ProductModel.is_available == True
                )
                products = session.exec(products_query).all()
                
                # Cache the result
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(POPULAR_PRODUCTS_CACHE_KEY, cache_data, ex=CACHE_TTL)
                
                # Mantener el orden de popularidad
                products_dict = {str(p.product_id): p for p in products}
                return [products_dict[pid] for pid in product_ids if pid in products_dict]
            
            return []
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching popular products: {str(e)}")

    @staticmethod
    async def get_user_favorite_products(
        user_id: UUID,
        session: Session,
        limit: int = 10
    ) -> List[ProductModel]:
        """Obtener productos favoritos de un usuario"""
        try:
            # Try to get from cache first
            cache_key = f"{USER_FAVORITES_CACHE_PREFIX}{user_id}"
            cached_data = await RedisClient.get_json(cache_key)
            if cached_data:
                product_ids = cached_data.get("product_ids", [])
                if product_ids:
                    query = select(ProductModel).where(
                        ProductModel.product_id.in_(product_ids),
                        ProductModel.is_available == True
                    )
                    return session.exec(query).all()
            
            # Get favorite products from database
            query = (
                select(ProductModel)
                .join(UserFavoriteModel, UserFavoriteModel.product_id == ProductModel.product_id)
                .where(
                    UserFavoriteModel.user_id == user_id,
                    ProductModel.is_available == True
                )
                .limit(limit)
            )
            
            products = session.exec(query).all()
            
            # Cache the result
            if products:
                product_ids = [str(p.product_id) for p in products]
                cache_data = {"product_ids": product_ids}
                await RedisClient.set_json(cache_key, cache_data, ex=CACHE_TTL)
            
            return products
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching favorite products: {str(e)}")
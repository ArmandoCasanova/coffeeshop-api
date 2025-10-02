from typing import Optional, List
from sqlmodel import Session, select, func
from fastapi import HTTPException
from uuid import UUID

from app.models.catalog.product_model import ProductModel
from app.api.products.product_schema import ProductCreateSchema, ProductUpdateSchema


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
            
            return new_product
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

    @staticmethod
    async def get_all_products(
        session: Session, 
        skip: int = 0, 
        limit: int = 10,
        is_available: Optional[bool] = None
    ) -> tuple[List[ProductModel], int]:
        """Obtener todos los productos con paginación"""
        try:
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
            
            return products, total
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
            
            return product
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
            
            return True
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")
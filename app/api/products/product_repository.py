from typing import Optional, List
from sqlmodel import Session, select, func
from uuid import UUID
from app.models.catalog.product_model import ProductModel

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_product(self, product_data: dict) -> ProductModel:
        try:
            new_product = ProductModel(**product_data)
            self.session.add(new_product)
            self.session.commit()
            self.session.refresh(new_product)
            return new_product
        except Exception:
            self.session.rollback()
            raise

    async def get_product_by_id(self, product_id: UUID) -> Optional[ProductModel]:
        try:
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = self.session.exec(statement).first()
            return product
        except Exception:
            raise

    async def get_all_products(
        self, 
        skip: int = 0, 
        limit: int = 10,
        is_available: Optional[bool] = None
    ) -> tuple[List[ProductModel], int]:
        try:
            query = select(ProductModel)
            
            if is_available is not None:
                query = query.where(ProductModel.is_available == is_available)
            
            total_query = select(func.count(ProductModel.product_id))
            if is_available is not None:
                total_query = total_query.where(ProductModel.is_available == is_available)
            
            total = self.session.exec(total_query).one()
            products = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return list(products), total
        except Exception:
            raise

    async def search_products_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[List[ProductModel], int]:
        try:
            search_pattern = f"%{name}%"
            query = select(ProductModel).where(ProductModel.name.ilike(search_pattern))
            
            total_query = select(func.count(ProductModel.product_id)).where(
                ProductModel.name.ilike(search_pattern)
            )
            
            total = self.session.exec(total_query).one()
            products = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return list(products), total
        except Exception:
            raise

    async def update_product(self, product_id: UUID, update_data: dict) -> Optional[ProductModel]:
        try:
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = self.session.exec(statement).first()
            
            if not product:
                return None
            
            for field, value in update_data.items():
                if hasattr(product, field) and value is not None:
                    setattr(product, field, value)
            
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception:
            self.session.rollback()
            raise

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            statement = select(ProductModel).where(ProductModel.product_id == product_id)
            product = self.session.exec(statement).first()
            
            if not product:
                return False
            
            self.session.delete(product)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

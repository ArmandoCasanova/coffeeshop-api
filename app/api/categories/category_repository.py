from typing import Optional, List, Dict, Any
from sqlmodel import Session, select, func, desc
from uuid import UUID
from app.models.catalog.product_category_model import ProductCategoryModel
import logging

logger = logging.getLogger(__name__)

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    # 🛑 NUEVO MÉTODO: Obtener categoría por nombre (para unicidad)
    def get_category_by_name(self, name: str) -> Optional[ProductCategoryModel]:
        """Busca una categoría por nombre (insensible a mayúsculas) para validación de unicidad."""
        try:
            # Usamos ilike() sin comodines para buscar una coincidencia exacta de nombre, 
            # pero insensible a mayúsculas/minúsculas.
            statement = select(ProductCategoryModel).where(
                ProductCategoryModel.name.ilike(name)
            )
            return self.session.exec(statement).first()
        except Exception as e:
            logger.exception("Error getting category by name in repository")
            raise

    def create_category(self, category_data: dict) -> ProductCategoryModel:
        """Crea una nueva categoría en la base de datos."""
        try:
            model_fields = ["name", "description", "image_url"]
            data_to_create = {k: v for k, v in category_data.items() if k in model_fields and v is not None}

            new_category = ProductCategoryModel(**data_to_create)
            self.session.add(new_category)
            self.session.commit()
            self.session.refresh(new_category)
            return new_category
        except Exception as e:
            logger.exception("Error creating category in repository")
            self.session.rollback()
            raise

    def get_category_by_id(self, category_id: UUID) -> Optional[ProductCategoryModel]:
        try:
            statement = select(ProductCategoryModel).where(ProductCategoryModel.category_id == category_id)
            return self.session.exec(statement).first()
        except Exception as e:
            logger.exception("Error getting category in repository")
            raise

    def get_all_categories(self, skip: int = 0, limit: int = 10) -> tuple[List[ProductCategoryModel], int]:
        try:
            query = select(ProductCategoryModel).order_by(desc(ProductCategoryModel.created_at))
            total_query = select(func.count(ProductCategoryModel.category_id))
            total = self.session.exec(total_query).one()
            categories = self.session.exec(query.offset(skip).limit(limit)).all()
            return list(categories), total
        except Exception as e:
            logger.exception("Error listing categories in repository")
            raise

    # 🔍 MÉTODO DE BÚSQUEDA (CORRECTO)
    def search_categories_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[List[ProductCategoryModel], int]:
        """Busca categorías por nombre parcial con paginación usando LIKE (funcional)."""
        try:
            search_pattern = f"%{name}%"
            # Consulta de datos con ilike (búsqueda parcial insensible a mayúsculas)
            query = select(ProductCategoryModel).where(ProductCategoryModel.name.ilike(search_pattern))
            
            # Consulta de conteo total
            total_query = select(func.count(ProductCategoryModel.category_id)).where(ProductCategoryModel.name.ilike(search_pattern))
            
            total = self.session.exec(total_query).one()
            categories = self.session.exec(query.offset(skip).limit(limit)).all()
            return list(categories), total
        except Exception as e:
            logger.exception("Error searching categories in repository")
            raise

    def update_category(self, category_id: UUID, update_data: dict) -> Optional[ProductCategoryModel]:
        try:
            statement = select(ProductCategoryModel).where(ProductCategoryModel.category_id == category_id)
            category = self.session.exec(statement).first()
            if not category:
                return None

            for field, value in update_data.items():
                if hasattr(category, field) and value is not None:
                    setattr(category, field, value)

            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)
            return category
        except Exception as e:
            logger.exception("Error updating category in repository")
            self.session.rollback()
            raise

    def delete_category(self, category_id: UUID) -> bool:
        try:
            statement = select(ProductCategoryModel).where(ProductCategoryModel.category_id == category_id)
            category = self.session.exec(statement).first()
            if not category:
                return False

            self.session.delete(category)
            self.session.commit()
            return True
        except Exception as e:
            logger.exception("Error deleting category in repository")
            self.session.rollback()
            raise
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.categories.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from app.api.categories.category_repository import CategoryRepository
from app.models.catalog.product_category_model import ProductCategoryModel
import logging

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self, session: Session):
        # Asumo que CategoryRepository usa la session para ejecutar consultas
        self.category_repository = CategoryRepository(session) 

    def create_category(self, category_data: CategoryCreateSchema) -> ProductCategoryModel:
        try:
            # 🛑 PASO CLAVE 1: VALIDACIÓN DE UNICIDAD por nombre
            # Intentamos encontrar una categoría existente con el mismo nombre (insensible a mayúsculas)
            existing_category = self.category_repository.get_category_by_name(
                name=category_data.name 
            )

            if existing_category:
                raise HTTPException(
                    status_code=409, 
                    detail=f"Ya existe una categoría con el nombre: {category_data.name}"
                )
                
            # Si es único, procedemos a la creación
            category_dict = category_data.model_dump()
            return self.category_repository.create_category(category_dict)
            
        except HTTPException:
            # Captura y relanza el 409
            raise
        except Exception as e:
            logger.exception("Error creating category in service")
            raise HTTPException(status_code=500, detail=str(e))

    def get_category_by_id(self, category_id: UUID) -> Optional[ProductCategoryModel]:
        try:
            return self.category_repository.get_category_by_id(category_id)
        except Exception as e:
            logger.exception("Error getting category in service")
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_categories(self, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            return self.category_repository.get_all_categories(skip, limit)
        except Exception as e:
            logger.exception("Error listing categories in service")
            raise HTTPException(status_code=500, detail=str(e))

    def update_category(self, category_id: UUID, category_data: CategoryUpdateSchema) -> Optional[ProductCategoryModel]:
        try:
            update_data = category_data.model_dump(exclude_unset=True)
            return self.category_repository.update_category(category_id, update_data)
        except Exception as e:
            logger.exception("Error updating category in service")
            raise HTTPException(status_code=500, detail=str(e))

    def delete_category(self, category_id: UUID) -> bool:
        try:
            return self.category_repository.delete_category(category_id)
        except Exception as e:
            logger.exception("Error deleting category in service")
            raise HTTPException(status_code=500, detail=str(e))

    # 🔍 PASO CLAVE 2: Llama al nuevo método del repositorio para la búsqueda
    def search_categories_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            # Asumo que el repositorio manejará la lógica LIKE y la paginación.
            return self.category_repository.search_categories_by_name(name, skip, limit)
        except Exception as e:
            logger.exception("Error searching categories in service")
            raise HTTPException(status_code=500, detail=str(e))
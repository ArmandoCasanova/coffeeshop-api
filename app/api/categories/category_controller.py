from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
import logging

from app.api.categories.category_service import CategoryService
from app.api.categories.category_schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    CategoryListResponseSchema,
)

logger = logging.getLogger(__name__)

class CategoryController:
    def __init__(self, session: Session):
        self.session = session
        self.service = CategoryService(session)

    # 1. 🛑 CORRECCIÓN: Manejo de unicidad (HTTP 409)
    def create_category(self, category_data: CategoryCreateSchema) -> CategoryResponseSchema:
        try:
            # Asumimos que CategoryService.create_category ahora valida unicidad
            # y puede lanzar una HTTPException 409 si la categoría ya existe.
            category = self.service.create_category(category_data)
            return CategoryResponseSchema.model_validate(category)
        except HTTPException as e:
            # Captura y relanza HTTPException si es un 409 (Conflicto)
            raise e
        except Exception as e:
            logger.exception("Error creating category")
            raise HTTPException(status_code=500, detail=str(e))

    def get_category(self, category_id: UUID) -> CategoryResponseSchema:
        try:
            category = self.service.get_category_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return CategoryResponseSchema.model_validate(category)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Error getting category")
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_categories(self, page: int = 1, page_size: int = 10) -> CategoryListResponseSchema:
        try:
            skip = (page - 1) * page_size
            categories, total = self.service.get_all_categories(skip, page_size)
            category_list = [CategoryResponseSchema.model_validate(c) for c in categories]
            return CategoryListResponseSchema(
                categories=category_list, total=total, page=page, page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Error getting all categories")
            raise HTTPException(status_code=500, detail=str(e))

    def update_category(self, category_id: UUID, category_data: CategoryUpdateSchema) -> CategoryResponseSchema:
        try:
            category = self.service.update_category(category_id, category_data)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return CategoryResponseSchema.model_validate(category)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Error updating category")
            raise HTTPException(status_code=500, detail=str(e))

    def delete_category(self, category_id: UUID) -> dict:
        try:
            deleted = self.service.delete_category(category_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Category not found")
            return {"message": "Category deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Error deleting category")
            raise HTTPException(status_code=500, detail=str(e))

    # 2. 🔍 CORRECCIÓN: El método está correcto, pero la lógica va en el servicio.
    def search_categories(self, name: str, page: int = 1, page_size: int = 10) -> CategoryListResponseSchema:
        try:
            skip = (page - 1) * page_size
            # La lógica de búsqueda LIKE debe estar implementada en search_categories_by_name
            categories, total = self.service.search_categories_by_name(name, skip, page_size) 
            category_list = [CategoryResponseSchema.model_validate(c) for c in categories]
            return CategoryListResponseSchema(
                categories=category_list, total=total, page=page, page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Error searching categories")
            raise HTTPException(status_code=500, detail=str(e))
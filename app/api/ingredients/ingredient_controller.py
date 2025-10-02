from typing import List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID

from app.api.ingredients.ingredient_service import IngredientService
from app.api.ingredients.ingredient_schema import (
    IngredientCreateSchema,
    IngredientUpdateSchema,
    IngredientResponseSchema,
    IngredientListResponseSchema,
    LowStockIngredientSchema,
    IngredientStockUpdateSchema
)


class IngredientController:
    def __init__(self, session: Session):
        self.session = session

    async def create_ingredient(self, ingredient_data: IngredientCreateSchema) -> IngredientResponseSchema:
        """Crear un nuevo ingrediente"""
        try:
            ingredient = await IngredientService.create_ingredient(ingredient_data, self.session)
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_ingredient(self, ingredient_id: UUID) -> IngredientResponseSchema:
        """Obtener un ingrediente por ID"""
        try:
            ingredient = await IngredientService.get_ingredient_by_id(ingredient_id, self.session)
            if not ingredient:
                raise HTTPException(status_code=404, detail="Ingredient not found")
            
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_ingredients(
        self, 
        page: int = 1, 
        page_size: int = 10
    ) -> IngredientListResponseSchema:
        """Obtener todos los ingredientes con paginación"""
        try:
            skip = (page - 1) * page_size
            ingredients, total = await IngredientService.get_all_ingredients(
                self.session, skip, page_size
            )
            
            ingredient_list = [IngredientResponseSchema.model_validate(ingredient) for ingredient in ingredients]
            
            return IngredientListResponseSchema(
                ingredients=ingredient_list,
                total=total,
                page=page,
                page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_ingredient(
        self, 
        ingredient_id: UUID, 
        ingredient_data: IngredientUpdateSchema
    ) -> IngredientResponseSchema:
        """Actualizar un ingrediente"""
        try:
            ingredient = await IngredientService.update_ingredient(
                ingredient_id, ingredient_data, self.session
            )
            if not ingredient:
                raise HTTPException(status_code=404, detail="Ingredient not found")
            
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_ingredient(self, ingredient_id: UUID) -> dict:
        """Eliminar un ingrediente"""
        try:
            deleted = await IngredientService.delete_ingredient(ingredient_id, self.session)
            if not deleted:
                raise HTTPException(status_code=404, detail="Ingredient not found")
            
            return {"message": "Ingredient deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_low_stock_ingredients(self) -> List[LowStockIngredientSchema]:
        """Obtener ingredientes con stock bajo"""
        try:
            ingredients = await IngredientService.get_low_stock_ingredients(self.session)
            
            low_stock_list = []
            for ingredient in ingredients:
                deficit = ingredient.stock_optimal_level - ingredient.stock_current_level
                low_stock_list.append(LowStockIngredientSchema(
                    ingredient_id=ingredient.ingredient_id,
                    name=ingredient.name,
                    stock_current_level=ingredient.stock_current_level,
                    stock_optimal_level=ingredient.stock_optimal_level,
                    deficit=deficit
                ))
            
            return low_stock_list
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_stock_level(
        self, 
        ingredient_id: UUID, 
        stock_data: IngredientStockUpdateSchema
    ) -> IngredientResponseSchema:
        """Actualizar solo el nivel de stock"""
        try:
            ingredient = await IngredientService.update_stock_level(
                ingredient_id, stock_data.stock_current_level, self.session
            )
            if not ingredient:
                raise HTTPException(status_code=404, detail="Ingredient not found")
            
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_ingredients(
        self, 
        name: str, 
        page: int = 1, 
        page_size: int = 10
    ) -> IngredientListResponseSchema:
        """Buscar ingredientes por nombre"""
        try:
            skip = (page - 1) * page_size
            ingredients, total = await IngredientService.search_ingredients_by_name(
                name, self.session, skip, page_size
            )
            
            ingredient_list = [IngredientResponseSchema.model_validate(ingredient) for ingredient in ingredients]
            
            return IngredientListResponseSchema(
                ingredients=ingredient_list,
                total=total,
                page=page,
                page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
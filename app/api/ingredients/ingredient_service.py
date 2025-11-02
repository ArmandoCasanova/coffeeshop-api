from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.ingredients.ingredient_schema import IngredientCreateSchema, IngredientUpdateSchema
from app.api.ingredients.ingredient_repository import IngredientRepository

class IngredientService:
    def __init__(self, session: Session):
        self.ingredient_repository = IngredientRepository(session)

    async def create_ingredient(self, ingredient_data: IngredientCreateSchema) -> object:
        try:
            ingredient_dict = ingredient_data.model_dump()
            return await self.ingredient_repository.create_ingredient(ingredient_dict)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating ingredient: {str(e)}")

    async def get_ingredient_by_id(self, ingredient_id: UUID) -> Optional[object]:
        try:
            return await self.ingredient_repository.get_ingredient_by_id(ingredient_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ingredient: {str(e)}")

    async def get_all_ingredients(self, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            return await self.ingredient_repository.get_all_ingredients(skip, limit)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ingredients: {str(e)}")

    async def update_ingredient(self, ingredient_id: UUID, ingredient_data: IngredientUpdateSchema) -> Optional[object]:
        try:
            update_data = ingredient_data.model_dump(exclude_unset=True)
            return await self.ingredient_repository.update_ingredient(ingredient_id, update_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating ingredient: {str(e)}")

    async def delete_ingredient(self, ingredient_id: UUID) -> bool:
        try:
            return await self.ingredient_repository.delete_ingredient(ingredient_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting ingredient: {str(e)}")

    async def get_low_stock_ingredients(self) -> list:
        try:
            return await self.ingredient_repository.get_low_stock_ingredients()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching low stock ingredients: {str(e)}")

    async def update_stock_level(self, ingredient_id: UUID, new_stock_level: int) -> Optional[object]:
        try:
            return await self.ingredient_repository.update_ingredient_stock(ingredient_id, new_stock_level)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating stock level: {str(e)}")

    async def search_ingredients_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[list, int]:
        try:
            return await self.ingredient_repository.search_ingredients_by_name(name, skip, limit)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching ingredients: {str(e)}")
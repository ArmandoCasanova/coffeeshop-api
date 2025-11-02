from app.core.http_response import CoffeeAppHttpResponse
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
        self.ingredient_service = IngredientService(session)

    async def create_ingredient(self, ingredient_data: IngredientCreateSchema) -> IngredientResponseSchema:
        try:
            ingredient = await self.ingredient_service.create_ingredient(ingredient_data)
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_ingredient(self, ingredient_id: UUID) -> IngredientResponseSchema:
        try:
            ingredient = await self.ingredient_service.get_ingredient_by_id(ingredient_id)
            if not ingredient:
                    CoffeeAppHttpResponse.not_found(message="Ingredient not found")
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_all_ingredients(self, page: int = 1, page_size: int = 10) -> IngredientListResponseSchema:
        try:
            skip = (page - 1) * page_size
            ingredients, total = await self.ingredient_service.get_all_ingredients(skip, page_size)
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

    async def update_ingredient(self, ingredient_id: UUID, ingredient_data: IngredientUpdateSchema) -> IngredientResponseSchema:
        try:
            ingredient = await self.ingredient_service.update_ingredient(ingredient_id, ingredient_data)
            if not ingredient:
                    CoffeeAppHttpResponse.not_found(message="Ingredient not found")
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def delete_ingredient(self, ingredient_id: UUID) -> dict:
        try:
            deleted = await self.ingredient_service.delete_ingredient(ingredient_id)
            if not deleted:
                    CoffeeAppHttpResponse.not_found(message="Ingredient not found")
            return {"message": "Ingredient deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def get_low_stock_ingredients(self) -> List[LowStockIngredientSchema]:
        try:
            ingredients = await self.ingredient_service.get_low_stock_ingredients()
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
                CoffeeAppHttpResponse.internal_error()

    async def update_stock_level(self, ingredient_id: UUID, stock_data: IngredientStockUpdateSchema) -> IngredientResponseSchema:
        try:
            ingredient = await self.ingredient_service.update_stock_level(ingredient_id, stock_data.stock_current_level)
            if not ingredient:
                    CoffeeAppHttpResponse.not_found(message="Ingredient not found")
            return IngredientResponseSchema.model_validate(ingredient)
        except HTTPException:
            raise
        except Exception as e:
                CoffeeAppHttpResponse.internal_error()

    async def search_ingredients(self, name: str, page: int = 1, page_size: int = 10) -> IngredientListResponseSchema:
        try:
            skip = (page - 1) * page_size
            ingredients, total = await self.ingredient_service.search_ingredients_by_name(name, skip, page_size)
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
                CoffeeAppHttpResponse.internal_error()
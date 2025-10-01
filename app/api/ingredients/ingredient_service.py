from typing import Optional, List
from sqlmodel import Session, select, func
from fastapi import HTTPException
from uuid import UUID

from app.models.inventory.ingredient_model import IngredientModel
from app.api.ingredients.ingredient_schema import (
    IngredientCreateSchema, 
    IngredientUpdateSchema,
    LowStockIngredientSchema
)


class IngredientService:
    @staticmethod
    async def create_ingredient(ingredient_data: IngredientCreateSchema, session: Session) -> IngredientModel:
        """Crear un nuevo ingrediente"""
        try:
            ingredient_dict = ingredient_data.model_dump()
            new_ingredient = IngredientModel(**ingredient_dict)
            
            session.add(new_ingredient)
            session.commit()
            session.refresh(new_ingredient)
            
            return new_ingredient
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating ingredient: {str(e)}")

    @staticmethod
    async def get_ingredient_by_id(ingredient_id: UUID, session: Session) -> Optional[IngredientModel]:
        """Obtener ingrediente por ID"""
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = session.exec(statement).first()
            return ingredient
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ingredient: {str(e)}")

    @staticmethod
    async def get_all_ingredients(
        session: Session, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[IngredientModel], int]:
        """Obtener todos los ingredientes con paginación"""
        try:
            # Count total
            count_query = select(func.count(IngredientModel.ingredient_id))
            total = session.exec(count_query).one()
            
            # Get paginated results
            query = select(IngredientModel).offset(skip).limit(limit).order_by(IngredientModel.name)
            ingredients = session.exec(query).all()
            
            return ingredients, total
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ingredients: {str(e)}")

    @staticmethod
    async def update_ingredient(
        ingredient_id: UUID, 
        ingredient_data: IngredientUpdateSchema, 
        session: Session
    ) -> Optional[IngredientModel]:
        """Actualizar un ingrediente"""
        try:
            # Get existing ingredient
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = session.exec(statement).first()
            
            if not ingredient:
                return None
            
            # Update fields
            update_data = ingredient_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(ingredient, field, value)
            
            # updated_at se actualiza automáticamente por BaseCoffeeAppModel
            session.add(ingredient)
            session.commit()
            session.refresh(ingredient)
            
            return ingredient
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating ingredient: {str(e)}")

    @staticmethod
    async def delete_ingredient(ingredient_id: UUID, session: Session) -> bool:
        """Eliminar un ingrediente"""
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = session.exec(statement).first()
            
            if not ingredient:
                return False
            
            session.delete(ingredient)
            session.commit()
            
            return True
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting ingredient: {str(e)}")

    @staticmethod
    async def get_low_stock_ingredients(session: Session) -> List[IngredientModel]:
        """Obtener ingredientes con stock bajo (current < optimal)"""
        try:
            statement = select(IngredientModel).where(
                IngredientModel.stock_current_level < IngredientModel.stock_optimal_level
            ).order_by(IngredientModel.stock_current_level)
            
            ingredients = session.exec(statement).all()
            return ingredients
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching low stock ingredients: {str(e)}")

    @staticmethod
    async def update_stock_level(
        ingredient_id: UUID, 
        new_stock_level: int, 
        session: Session
    ) -> Optional[IngredientModel]:
        """Actualizar solo el nivel de stock de un ingrediente"""
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = session.exec(statement).first()
            
            if not ingredient:
                return None
            
            ingredient.stock_current_level = new_stock_level
            # updated_at se actualiza automáticamente por BaseCoffeeAppModel
            
            session.add(ingredient)
            session.commit()
            session.refresh(ingredient)
            
            return ingredient
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating stock level: {str(e)}")

    @staticmethod
    async def search_ingredients_by_name(
        name: str, 
        session: Session, 
        skip: int = 0, 
        limit: int = 10
    ) -> tuple[List[IngredientModel], int]:
        """Buscar ingredientes por nombre"""
        try:
            # Search query (case insensitive)
            search_pattern = f"%{name}%"
            query = select(IngredientModel).where(IngredientModel.name.ilike(search_pattern))
            
            # Count total
            count_query = select(func.count(IngredientModel.ingredient_id)).where(
                IngredientModel.name.ilike(search_pattern)
            )
            total = session.exec(count_query).one()
            
            # Get paginated results
            query = query.offset(skip).limit(limit).order_by(IngredientModel.name)
            ingredients = session.exec(query).all()
            
            return ingredients, total
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching ingredients: {str(e)}")
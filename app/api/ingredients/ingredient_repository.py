from typing import Optional, List
from sqlmodel import Session, select, func
from uuid import UUID
from app.models.inventory.ingredient_model import IngredientModel

class IngredientRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_ingredient(self, ingredient_data: dict) -> IngredientModel:
        try:
            new_ingredient = IngredientModel(**ingredient_data)
            self.session.add(new_ingredient)
            self.session.commit()
            self.session.refresh(new_ingredient)
            return new_ingredient
        except Exception:
            self.session.rollback()
            raise

    async def get_ingredient_by_id(self, ingredient_id: UUID) -> Optional[IngredientModel]:
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = self.session.exec(statement).first()
            return ingredient
        except Exception:
            raise

    async def get_all_ingredients(self, skip: int = 0, limit: int = 10) -> tuple[List[IngredientModel], int]:
        try:
            query = select(IngredientModel)
            total_query = select(func.count(IngredientModel.ingredient_id))
            
            total = self.session.exec(total_query).one()
            ingredients = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return list(ingredients), total
        except Exception:
            raise

    async def search_ingredients_by_name(self, name: str, skip: int = 0, limit: int = 10) -> tuple[List[IngredientModel], int]:
        try:
            search_pattern = f"%{name}%"
            query = select(IngredientModel).where(IngredientModel.name.ilike(search_pattern))
            
            total_query = select(func.count(IngredientModel.ingredient_id)).where(
                IngredientModel.name.ilike(search_pattern)
            )
            
            total = self.session.exec(total_query).one()
            ingredients = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return list(ingredients), total
        except Exception:
            raise

    async def update_ingredient(self, ingredient_id: UUID, update_data: dict) -> Optional[IngredientModel]:
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = self.session.exec(statement).first()
            
            if not ingredient:
                return None
            
            for field, value in update_data.items():
                if hasattr(ingredient, field) and value is not None:
                    setattr(ingredient, field, value)
            
            self.session.add(ingredient)
            self.session.commit()
            self.session.refresh(ingredient)
            return ingredient
        except Exception:
            self.session.rollback()
            raise

    async def delete_ingredient(self, ingredient_id: UUID) -> bool:
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = self.session.exec(statement).first()
            
            if not ingredient:
                return False
            
            self.session.delete(ingredient)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    async def get_low_stock_ingredients(self) -> List[IngredientModel]:
        try:
            query = select(IngredientModel).where(
                IngredientModel.stock_current_level < IngredientModel.stock_optimal_level
            )
            ingredients = self.session.exec(query).all()
            return list(ingredients)
        except Exception:
            raise

    async def update_ingredient_stock(self, ingredient_id: UUID, new_stock_level: int) -> Optional[IngredientModel]:
        try:
            statement = select(IngredientModel).where(IngredientModel.ingredient_id == ingredient_id)
            ingredient = self.session.exec(statement).first()
            
            if not ingredient:
                return None
            
            ingredient.stock_current_level = new_stock_level
            self.session.add(ingredient)
            self.session.commit()
            self.session.refresh(ingredient)
            return ingredient
        except Exception:
            self.session.rollback()
            raise

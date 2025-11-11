from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.api.ingredients.ingredient_controller import IngredientController
from app.api.ingredients.ingredient_schema import (
    IngredientCreateSchema,
    IngredientUpdateSchema,
    IngredientResponseSchema,
    IngredientListResponseSchema,
    LowStockIngredientSchema,
    IngredientStockUpdateSchema
)

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.post("", response_model=IngredientResponseSchema)
async def create_ingredient(
    ingredient_data: IngredientCreateSchema,
    session: Session = Depends(get_db)
):
    """Crear un nuevo ingrediente"""
    controller = IngredientController(session)
    return await controller.create_ingredient(ingredient_data)


@router.get("", response_model=IngredientListResponseSchema)
async def get_all_ingredients(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    session: Session = Depends(get_db)
):
    """Obtener todos los ingredientes con paginación"""
    controller = IngredientController(session)
    return await controller.get_all_ingredients(page, page_size)


@router.get("/search", response_model=IngredientListResponseSchema)
async def search_ingredients(
    name: str = Query(..., description="Nombre del ingrediente a buscar"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    session: Session = Depends(get_db)
):
    """Buscar ingredientes por nombre"""
    controller = IngredientController(session)
    return await controller.search_ingredients(name, page, page_size)


@router.get("/low-stock", response_model=List[LowStockIngredientSchema])
async def get_low_stock_ingredients(
    session: Session = Depends(get_db)
):
    """Obtener ingredientes con stock bajo"""
    controller = IngredientController(session)
    return await controller.get_low_stock_ingredients()


@router.get("/{ingredient_id}", response_model=IngredientResponseSchema)
async def get_ingredient(
    ingredient_id: UUID,
    session: Session = Depends(get_db)
):
    """Obtener un ingrediente por ID"""
    controller = IngredientController(session)
    return await controller.get_ingredient(ingredient_id)


@router.put("/{ingredient_id}", response_model=IngredientResponseSchema)
async def update_ingredient(
    ingredient_id: UUID,
    ingredient_data: IngredientUpdateSchema,
    session: Session = Depends(get_db)
):
    """Actualizar un ingrediente"""
    controller = IngredientController(session)
    return await controller.update_ingredient(ingredient_id, ingredient_data)


@router.patch("/{ingredient_id}/stock", response_model=IngredientResponseSchema)
async def update_stock_level(
    ingredient_id: UUID,
    stock_data: IngredientStockUpdateSchema,
    session: Session = Depends(get_db)
):
    """Actualizar solo el nivel de stock de un ingrediente"""
    controller = IngredientController(session)
    return await controller.update_stock_level(ingredient_id, stock_data)


@router.delete("/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: UUID,
    session: Session = Depends(get_db)
):
    """Eliminar un ingrediente"""
    controller = IngredientController(session)
    return await controller.delete_ingredient(ingredient_id)
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.api.categories.category_controller import CategoryController
from app.core.database import get_db

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.get("/")
async def get_all_categories(session: Session = Depends(get_db)):
    """
    Obtener todas las categorías.
    """
    controller = CategoryController(session)
    categories = await controller.get_all_categories()
    return categories

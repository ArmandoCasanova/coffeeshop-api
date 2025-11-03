from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.api.categories.category_controller import CategoryController
from app.core.database import get_db
from app.models.catalog.product_category_model import ProductCategoryModel

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@router.get("/", response_model=list[ProductCategoryModel])
async def get_all_categories(session: Session = Depends(get_db)):
    """Obtener todas las categorías."""
    controller = CategoryController(session)
    return await controller.get_all_categories()

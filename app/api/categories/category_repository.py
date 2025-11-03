from sqlmodel import Session, select
from app.models.catalog.product_category_model import ProductCategoryModel


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_all_categories(self) -> list[ProductCategoryModel]:
        """Obtiene todas las categorías registradas."""
        statement = select(ProductCategoryModel)
        return self.session.exec(statement).all()

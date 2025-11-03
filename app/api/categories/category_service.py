from sqlmodel import Session
from app.api.categories.category_repository import CategoryRepository
from app.core.http_response import CoffeeAppHttpResponse


class CategoryService:
    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)

    async def get_all_categories(self):
        try:
            categories = await self.repository.get_all_categories()
            return CoffeeAppHttpResponse.ok(categories)
        except Exception as e:
            print("❌ Error en get_all_categories:", e)
            CoffeeAppHttpResponse.internal_error()

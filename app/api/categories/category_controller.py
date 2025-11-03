from app.api.categories.category_service import CategoryService


class CategoryController:
    def __init__(self, session):
        self.service = CategoryService(session)

    async def get_all_categories(self):
        return await self.service.get_all_categories()

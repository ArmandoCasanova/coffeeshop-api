from typing import Optional, List, Dict, Any
from sqlmodel import Session, select, func
from uuid import UUID
from datetime import datetime, timedelta
from app.models.catalog.product_model import ProductModel
from app.models.catalog.product_category_model import ProductCategoryModel
from app.models.catalog.product_category_link_model import ProductCategoryLinkModel
from app.models.orders.order_item_model import OrderItemModel
from app.models.orders.order_model import OrderModel
from app.models.users.user_favorite_model import UserFavoriteModel


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_product(self, product_data: dict) -> ProductModel:
        try:
            new_product = ProductModel(**product_data)
            self.session.add(new_product)
            self.session.commit()
            self.session.refresh(new_product)
            return new_product
        except Exception:
            self.session.rollback()
            raise

    async def get_product_by_id(self, product_id: UUID) -> Optional[ProductModel]:
        try:
            statement = select(ProductModel).where(
                ProductModel.product_id == product_id
            )
            product = self.session.exec(statement).first()
            return product
        except Exception:
            raise

    async def get_all_products(
        self, skip: int = 0, limit: int = 10, is_available: Optional[bool] = None
    ) -> tuple[List[ProductModel], int]:
        try:
            query = select(ProductModel).order_by(ProductModel.created_at.desc())

            if is_available is not None:
                query = query.where(ProductModel.is_available == is_available)

            total_query = select(func.count(ProductModel.product_id))
            if is_available is not None:
                total_query = total_query.where(
                    ProductModel.is_available == is_available
                )

            total = self.session.exec(total_query).one()
            products = self.session.exec(query.offset(skip).limit(limit)).all()

            return list(products), total
        except Exception:
            raise

    async def search_products_by_name(
        self, name: str, skip: int = 0, limit: int = 10
    ) -> tuple[List[ProductModel], int]:
        try:
            search_pattern = f"%{name}%"
            query = select(ProductModel).where(ProductModel.name.ilike(search_pattern))

            total_query = select(func.count(ProductModel.product_id)).where(
                ProductModel.name.ilike(search_pattern)
            )

            total = self.session.exec(total_query).one()
            products = self.session.exec(query.offset(skip).limit(limit)).all()

            return list(products), total
        except Exception:
            raise

    async def update_product(
        self, product_id: UUID, update_data: dict
    ) -> Optional[ProductModel]:
        try:
            statement = select(ProductModel).where(
                ProductModel.product_id == product_id
            )
            product = self.session.exec(statement).first()

            if not product:
                return None

            for field, value in update_data.items():
                if hasattr(product, field) and value is not None:
                    setattr(product, field, value)

            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception:
            self.session.rollback()
            raise

    async def delete_product(self, product_id: UUID) -> bool:
        try:
            statement = select(ProductModel).where(
                ProductModel.product_id == product_id
            )
            product = self.session.exec(statement).first()

            if not product:
                return False

            self.session.delete(product)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def get_popular_products(
        self, limit: int = 10, days: int = 7
    ) -> List[ProductModel]:
        """
        Get popular products based on sales from the last N days.

        Args:
            limit: Maximum number of products to return
            days: Number of days to look back for sales data

        Returns:
            List of ProductModel ordered by popularity (most sold first)
        """
        try:
            date_threshold = datetime.utcnow() - timedelta(days=days)

            subquery = (
                select(
                    OrderItemModel.product_id,
                    func.sum(OrderItemModel.quantity).label("total_sold"),
                )
                .join(OrderModel, OrderItemModel.order_id == OrderModel.order_id)
                .where(OrderModel.order_date >= date_threshold)
                .where(OrderModel.status != "cancelled")
                .group_by(OrderItemModel.product_id)
                .order_by(func.sum(OrderItemModel.quantity).desc())
                .limit(limit)
            )

            result = self.session.exec(subquery).all()
            product_ids = [row[0] for row in result]

            if not product_ids:
                return []

            products_query = select(ProductModel).where(
                ProductModel.product_id.in_(product_ids),
                ProductModel.is_available == True,
            )
            products = self.session.exec(products_query).all()

            product_dict = {p.product_id: p for p in products}
            sorted_products = [
                product_dict[pid] for pid in product_ids if pid in product_dict
            ]

            return sorted_products
        except Exception:
            raise

    def get_products_by_ids(
        self, product_ids: List[UUID], is_available: Optional[bool] = True
    ) -> List[ProductModel]:
        """
        Get products by a list of product IDs.

        Args:
            product_ids: List of product UUIDs to retrieve
            is_available: Filter by availability (None = all, True = available, False = unavailable)

        Returns:
            List of ProductModel instances
        """
        try:
            if not product_ids:
                return []

            uuid_list = [
                UUID(pid) if isinstance(pid, str) else pid for pid in product_ids
            ]

            query = select(ProductModel).where(ProductModel.product_id.in_(uuid_list))

            if is_available is not None:
                query = query.where(ProductModel.is_available == is_available)

            products = self.session.exec(query).all()
            return list(products)
        except Exception:
            raise

    def get_user_favorite_products(
        self, user_id: UUID, limit: int = 10
    ) -> List[ProductModel]:
        """
        Get favorite products for a specific user.

        Args:
            user_id: UUID of the user
            limit: Maximum number of favorite products to return

        Returns:
            List of ProductModel instances that are in the user's favorites
        """
        try:
            query = (
                select(ProductModel)
                .join(
                    UserFavoriteModel,
                    ProductModel.product_id == UserFavoriteModel.product_id,
                )
                .where(UserFavoriteModel.user_id == user_id)
                .where(ProductModel.is_available == True)
                .limit(limit)
            )

            products = self.session.exec(query).all()
            return list(products)
        except Exception:
            raise

    def get_popular_categories(
        self, limit: int = 10, days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get popular categories based on sales from the last N days.
        If there are fewer categories with sales than the limit, fill with categories without sales.

        Args:
            limit: Maximum number of categories to return
            days: Number of days to look back for sales data

        Returns:
            List of dictionaries with category info and sales count
        """
        try:
            date_threshold = datetime.utcnow() - timedelta(days=days)

            query_with_sales = (
                select(
                    ProductCategoryModel.category_id,
                    ProductCategoryModel.name,
                    ProductCategoryModel.description,
                    ProductCategoryModel.image_url,
                    func.sum(OrderItemModel.quantity).label("total_sales"),
                )
                .join(
                    ProductCategoryLinkModel,
                    ProductCategoryModel.category_id
                    == ProductCategoryLinkModel.category_id,
                )
                .join(
                    ProductModel,
                    ProductCategoryLinkModel.product_id == ProductModel.product_id,
                )
                .join(
                    OrderItemModel, ProductModel.product_id == OrderItemModel.product_id
                )
                .join(OrderModel, OrderItemModel.order_id == OrderModel.order_id)
                .where(OrderModel.order_date >= date_threshold)
                .where(OrderModel.status != "cancelled")
                .group_by(
                    ProductCategoryModel.category_id,
                    ProductCategoryModel.name,
                    ProductCategoryModel.description,
                    ProductCategoryModel.image_url,
                )
                .order_by(func.sum(OrderItemModel.quantity).desc())
            )

            result_with_sales = self.session.exec(query_with_sales).all()

            categories = []
            category_ids_with_sales = set()

            for row in result_with_sales:
                categories.append(
                    {
                        "category_id": str(row[0]),
                        "name": row[1],
                        "description": row[2],
                        "image_url": row[3],
                        "total_sales": int(row[4]),
                    }
                )
                category_ids_with_sales.add(row[0])

            if len(categories) < limit:
                remaining_limit = limit - len(categories)


                query_without_sales = (
                    select(
                        ProductCategoryModel.category_id,
                        ProductCategoryModel.name,
                        ProductCategoryModel.description,
                        ProductCategoryModel.image_url,
                    )
                    .where(
                        ProductCategoryModel.category_id.not_in(category_ids_with_sales)
                    )
                    .order_by(ProductCategoryModel.name)
                    .limit(remaining_limit)
                )

                result_without_sales = self.session.exec(query_without_sales).all()

                for row in result_without_sales:
                    categories.append(
                        {
                            "category_id": str(row[0]),
                            "name": row[1],
                            "description": row[2],
                            "image_url": row[3],
                            "total_sales": 0,
                        }
                    )
            return categories[:limit]
        except Exception:
            raise

from typing import Optional, List, Dict, Any
from sqlmodel import Session, select, func
from uuid import UUID
from datetime import datetime, timedelta
from app.models.catalog.product_model import ProductModel
from app.models.catalog.product_category_model import ProductCategoryModel
from app.models.catalog.product_category_link_model import ProductCategoryLinkModel
from app.models.inventory.product_ingredient_model import ProductIngredientModel
from app.models.customization.product_customization_group_model import ProductCustomizationGroupModel
from app.models.customization.customization_group_model import CustomizationGroupModel
from app.models.customization.customization_option_model import CustomizationOptionModel
from app.models.inventory.ingredient_model import IngredientModel
from app.models.orders.order_item_model import OrderItemModel
from app.models.orders.order_model import OrderModel
from app.models.users.user_favorite_model import UserFavoriteModel


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_product(self, product_data: dict) -> ProductModel:
        try:
            category_ids = product_data.pop('category_ids', [])
            customization_group_ids = product_data.pop('customization_group_ids', [])
            ingredients = product_data.pop('ingredients', [])
            

            new_product = ProductModel(**product_data)
            self.session.add(new_product)
            self.session.flush()  
            

            for category_id in category_ids:
                category_link = ProductCategoryLinkModel(
                    product_id=new_product.product_id,
                    category_id=category_id
                )
                self.session.add(category_link)
            

            for group_id in customization_group_ids:
                group_link = ProductCustomizationGroupModel(
                    product_id=new_product.product_id,
                    group_id=group_id
                )
                self.session.add(group_link)
            

            for ingredient in ingredients:
                ingredient_link = ProductIngredientModel(
                    product_id=new_product.product_id,
                    ingredient_id=ingredient['ingredient_id'],
                    quantity_required=float(ingredient['quantity_required'])
                )
                self.session.add(ingredient_link)
            
            new_product.category_info_json = self._build_category_json(category_ids)
            new_product.customization_details_json = self._build_customization_json(customization_group_ids)
            new_product.ingredients_json = self._build_ingredients_json(ingredients)
            
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

            category_ids = update_data.pop('category_ids', None)
            customization_group_ids = update_data.pop('customization_group_ids', None)
            ingredients = update_data.pop('ingredients', None)
            
            for field, value in update_data.items():
                if hasattr(product, field) and value is not None:
                    setattr(product, field, value)
            
            if category_ids is not None:
                self.session.exec(
                    select(ProductCategoryLinkModel).where(
                        ProductCategoryLinkModel.product_id == product_id
                    )
                ).all()
                for link in self.session.exec(
                    select(ProductCategoryLinkModel).where(
                        ProductCategoryLinkModel.product_id == product_id
                    )
                ).all():
                    self.session.delete(link)
                
                for category_id in category_ids:
                    category_link = ProductCategoryLinkModel(
                        product_id=product_id,
                        category_id=category_id
                    )
                    self.session.add(category_link)
                
                product.category_info_json = self._build_category_json(category_ids)
            
            if customization_group_ids is not None:
                for link in self.session.exec(
                    select(ProductCustomizationGroupModel).where(
                        ProductCustomizationGroupModel.product_id == product_id
                    )
                ).all():
                    self.session.delete(link)
                
                for group_id in customization_group_ids:
                    group_link = ProductCustomizationGroupModel(
                        product_id=product_id,
                        group_id=group_id
                    )
                    self.session.add(group_link)
                
                product.customization_details_json = self._build_customization_json(customization_group_ids)
            
            if ingredients is not None:
                for link in self.session.exec(
                    select(ProductIngredientModel).where(
                        ProductIngredientModel.product_id == product_id
                    )
                ).all():
                    self.session.delete(link)
                
                for ingredient in ingredients:
                    ingredient_link = ProductIngredientModel(
                        product_id=product_id,
                        ingredient_id=ingredient['ingredient_id'],
                        quantity_required=float(ingredient['quantity_required'])
                    )
                    self.session.add(ingredient_link)
                
                product.ingredients_json = self._build_ingredients_json(ingredients)

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
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            # Marcar como no disponible en lugar de eliminar (soft delete)
            product.is_available = False
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return True
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            import traceback
            traceback.print_exc()
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

    def _build_category_json(self, category_ids: List[UUID]) -> Dict[str, Any]:
        """Build category_info_json from category IDs for UI reading"""
        if not category_ids:
            return {}
        
        categories = self.session.exec(
            select(ProductCategoryModel).where(
                ProductCategoryModel.category_id.in_(category_ids)
            )
        ).all()
        
        if not categories:
            return {}
        
        categories_list = []
        for category in categories:
            categories_list.append({
                "category_id": str(category.category_id),
                "category_name": category.name
            })
        
        primary = categories_list[0] if categories_list else {}
        
        return {
            "category_id": primary.get("category_id", ""),
            "category_name": primary.get("category_name", ""),
            "categories": categories_list  
        }
    
    def _build_customization_json(self, group_ids: List[UUID]) -> Dict[str, Any]:
        """Build customization_details_json from group IDs for UI reading"""
        if not group_ids:
            return {}
        
        customization_details = {}
        
        for group_id in group_ids:
            group = self.session.exec(
                select(CustomizationGroupModel).where(
                    CustomizationGroupModel.group_id == group_id
                )
            ).first()
            
            if not group:
                continue
            
            options = self.session.exec(
                select(CustomizationOptionModel).where(
                    CustomizationOptionModel.group_id == group_id
                )
            ).all()
            
            options_list = []
            for option in options:
                option_data = {
                    "option_id": str(option.option_id),
                    "name": option.name,
                    "extra_cost": float(option.extra_cost),
                    "is_size_option": option.is_size_option,
                    "details": option.details or ""
                }
                
                if option.consumed_ingredient_id:
                    ingredient = self.session.exec(
                        select(IngredientModel).where(
                            IngredientModel.ingredient_id == option.consumed_ingredient_id
                        )
                    ).first()
                    
                    if ingredient:
                        option_data["consumed_ingredient"] = {
                            "ingredient_id": str(option.consumed_ingredient_id),
                            "ingredient_name": ingredient.name,
                            "quantity_consumed": float(option.quantity_consumed),
                            "unit": ingredient.unit_of_measure
                        }
                
                options_list.append(option_data)
            
            customization_details[group.system_name] = {
                "group_id": str(group.group_id),
                "system_name": group.system_name,
                "display_name": group.display_name,
                "options": options_list
            }
        
        return customization_details
    
    def _build_ingredients_json(self, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build ingredients_json from ingredient list for UI reading"""
        if not ingredients:
            return {}
        
        ingredients_list = []
        
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['ingredient_id']
            quantity = float(ingredient_data['quantity_required'])
            
            ingredient = self.session.exec(
                select(IngredientModel).where(
                    IngredientModel.ingredient_id == ingredient_id
                )
            ).first()
            
            if not ingredient:
                continue
            
            ingredients_list.append({
                "ingredientId": str(ingredient.ingredient_id),
                "quantity": quantity,
                "unit": ingredient.unit_of_measure
            })
        
        return {
            "ingredients": ingredients_list
        }

    async def check_is_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            existing = self.session.exec(
                select(UserFavoriteModel).where(
                    UserFavoriteModel.user_id == user_id,
                    UserFavoriteModel.product_id == product_id
                )
            ).first()
            return existing is not None
        except Exception:
            raise

    async def add_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            existing = self.session.exec(
                select(UserFavoriteModel).where(
                    UserFavoriteModel.user_id == user_id,
                    UserFavoriteModel.product_id == product_id
                )
            ).first()
            
            if existing:
                return False
            
            favorite = UserFavoriteModel(user_id=user_id, product_id=product_id)
            self.session.add(favorite)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    async def remove_favorite(self, user_id: UUID, product_id: UUID) -> bool:
        try:
            favorite = self.session.exec(
                select(UserFavoriteModel).where(
                    UserFavoriteModel.user_id == user_id,
                    UserFavoriteModel.product_id == product_id
                )
            ).first()
            
            if not favorite:
                return False
            
            self.session.delete(favorite)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    async def get_user_favorites(self, user_id: UUID) -> list[UserFavoriteModel]:
        """Obtener todos los favoritos de un usuario"""
        try:
            favorites = self.session.exec(
                select(UserFavoriteModel).where(UserFavoriteModel.user_id == user_id)
            ).all()
            return favorites
        except Exception:
            raise


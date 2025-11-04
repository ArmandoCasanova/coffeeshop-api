from sqlmodel import Session, select, func
from uuid import UUID
from typing import Optional, Tuple, List

from app.models.orders.order_model import OrderModel, OrderStatus, PaymentType
from app.models.orders.order_item_model import OrderItemModel
from app.models.orders.order_item_customization_model import OrderItemCustomizationModel
from app.models.users.user_model import UserModel
from .order_schema import OrderItemCustomizationCreateSchema


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_order(
        self,
        user_id: UUID,
        total_amount: float,
        points_earned: float,
        payment_type,
        items_summary_json: list,
    ) -> OrderModel:
        """Create a new order"""
        order = OrderModel(
            user_id=user_id,
            status=OrderStatus.pending,
            total_amount=total_amount,
            points_earned=points_earned,
            payment_type=payment_type,
            items_summary_json=items_summary_json,
        )
        self.session.add(order)
        self.session.flush()
        return order

    async def create_order_item(
        self,
        order_id: UUID,
        product_id: UUID,
        quantity: int,
        price_at_purchase: float,
        details: Optional[str],
        customizations: List[OrderItemCustomizationCreateSchema],
    ) -> OrderItemModel:
        """Create an order item with customizations"""
        order_item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=price_at_purchase,
            details=details,
        )
        self.session.add(order_item)
        self.session.flush()

        # Add customizations
        for customization in customizations:
            item_customization = OrderItemCustomizationModel(
                order_item_id=order_item.order_item_id,
                option_id=customization.option_id,
                extra_cost_at_purchase=customization.extra_cost_at_purchase,
            )
            self.session.add(item_customization)

        return order_item

    async def get_all_orders(
        self, page: int, page_size: int, status: Optional[OrderStatus]
    ) -> Tuple[List[Tuple[OrderModel, UserModel]], int]:
        """Get all orders with pagination and optional status filter"""
        query = select(OrderModel, UserModel).join(
            UserModel, OrderModel.user_id == UserModel.user_id
        )

        if status:
            query = query.where(OrderModel.status == status)

        query = query.order_by(OrderModel.order_date.desc())

        total_count_query = select(func.count()).select_from(query.subquery())
        total_count = self.session.exec(total_count_query).one()

        paginated_query = query.offset((page - 1) * page_size).limit(page_size)
        results = self.session.exec(paginated_query).all()

        return results, total_count

    async def get_user_orders(
        self, user_id: UUID, page: int, page_size: int
    ) -> Tuple[List[Tuple[OrderModel, UserModel]], int]:
        """Get orders for a specific user"""
        query = (
            select(OrderModel, UserModel)
            .join(UserModel, OrderModel.user_id == UserModel.user_id)
            .where(OrderModel.user_id == user_id)
            .order_by(OrderModel.order_date.desc())
        )

        total_count_query = select(func.count()).select_from(query.subquery())
        total_count = self.session.exec(total_count_query).one()

        paginated_query = query.offset((page - 1) * page_size).limit(page_size)
        results = self.session.exec(paginated_query).all()

        return results, total_count

    async def get_order_by_id(
        self, order_id: UUID
    ) -> Optional[Tuple[OrderModel, UserModel]]:
        """Get a specific order by ID"""
        query = (
            select(OrderModel, UserModel)
            .join(UserModel, OrderModel.user_id == UserModel.user_id)
            .where(OrderModel.order_id == order_id)
        )
        result = self.session.exec(query).first()
        return result

    async def update_order_status(
        self, order_id: UUID, status: OrderStatus
    ) -> Optional[OrderModel]:
        """Update order status"""
        order = self.session.get(OrderModel, order_id)
        if not order:
            return None

        order.status = status
        self.session.add(order)
        self.session.flush()
        return order

    async def update_order_payment_type(
        self, order_id: UUID, payment_type: PaymentType
    ) -> Optional[OrderModel]:
        """Update order payment type"""
        order = self.session.get(OrderModel, order_id)
        if not order:
            return None

        order.payment_type = payment_type
        self.session.add(order)
        self.session.flush()
        return order

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order and all its items"""
        order = self.session.get(OrderModel, order_id)
        if not order:
            return False

        # Delete order items and their customizations (cascade should handle this)
        statement = select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        items = self.session.exec(statement).all()

        for item in items:
            # Delete customizations first
            customization_statement = select(OrderItemCustomizationModel).where(
                OrderItemCustomizationModel.order_item_id == item.order_item_id
            )
            customizations = self.session.exec(customization_statement).all()
            for customization in customizations:
                self.session.delete(customization)

            self.session.delete(item)

        self.session.flush()
        self.session.delete(order)
        self.session.flush()
        return True

    async def get_user(self, user_id: UUID) -> Optional[UserModel]:
        """Get user by ID"""
        return self.session.get(UserModel, user_id)

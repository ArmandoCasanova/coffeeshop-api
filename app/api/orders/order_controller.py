from sqlmodel import Session, select, func
from uuid import UUID
from fastapi import HTTPException

from app.models.orders.order_model import OrderModel, OrderStatus
from app.models.users.user_model import UserModel

from .order_schema import OrderResponseSchema, OrderUpdateStatusSchema


class OrderController:
    def __init__(self, session: Session):
        self.session = session

    async def get_all_orders(
        self, page: int, page_size: int, status: OrderStatus | None
    ):
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

        orders_list = []
        for order, user in results:
            order_data = order.model_dump()
            order_data["user"] = user
            orders_list.append(OrderResponseSchema.model_validate(order_data))

        return {
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "orders": orders_list,
        }

    async def update_order_status(self, order_id: UUID, data: OrderUpdateStatusSchema):
        order = self.session.get(OrderModel, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = data.status
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        user = self.session.get(UserModel, order.user_id)
        order_data = order.model_dump()
        order_data["user"] = user
        return OrderResponseSchema.model_validate(order_data)

    async def delete_order(self, order_id: UUID):
        order = self.session.get(OrderModel, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        self.session.delete(order)
        self.session.commit()
        return {"message": "Order deleted successfully"}

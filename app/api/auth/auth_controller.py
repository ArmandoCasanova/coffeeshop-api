from sqlmodel import UUID, Session, select
from fastapi import HTTPException
from app.core.http_response import CoffeeAppHttpResponse
from pydantic import EmailStr

from app.api.auth.auth_service import AuthService
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema
from app.models.orders.order_item_model import OrderItemModel
from app.models.orders.order_model import OrderModel


class AuthController:
    def __init__(self, session: Session):
        self.auth_service = AuthService(session)

    async def signup(self, data: SignupSchema) -> AuthResponseSchema:
        try:
            user = await self.auth_service.signup_user(data)
            tokens = self.auth_service.generate_tokens_for_user(user)
            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException as e:
            raise e

    async def login(self, email: EmailStr, password: str) -> AuthResponseSchema:
        try:
            user = await self.auth_service.authenticate_user(email, password)
            tokens = self.auth_service.generate_tokens_for_user(user)
            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException as e:
            raise e
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def delete_order(self, order_id: UUID) -> dict:
        """
        Borra una orden y todos sus items asociados.
        """

        # 1. Buscar la orden
        order = self.session.get(OrderModel, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        statement = select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        items = self.session.exec(statement).all()

        for item in items:
            self.session.delete(item)

        try:
            self.session.flush()
        except Exception as e:

            self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error deleting order items: {str(e)}"
            )

        self.session.delete(order)

        try:
            self.session.commit()
        except Exception as e:

            self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error committing order deletion: {str(e)}"
            )

        return {"message": "Order deleted successfully"}

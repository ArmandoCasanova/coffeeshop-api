from sqlmodel import Session
from fastapi import HTTPException
from app.core.http_response import CoffeeAppHttpResponse
from pydantic import EmailStr

from app.api.auth.auth_service import AuthService
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema


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

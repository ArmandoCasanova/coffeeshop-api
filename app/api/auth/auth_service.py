from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session
from fastapi import HTTPException
from pydantic import EmailStr

from app.models.users.user_model import UserModel
from app.constants.user_constants import UserRoles
from app.constants.response_codes import CoffeeAppResponseCodes
from app.core.http_response import CoffeeAppHttpResponse
from app.utils.security import get_password_hash, verify_password, get_user_token
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema
from app.api.auth.auth_repository import AuthRepository


class AuthService:
    """
    Operaciones entre repositories y aplica reglas de negocio.
    """
    
    def __init__(self, session: Session):
        self.auth_repository = AuthRepository(session)
    
    async def signup_user(self, user_data: SignupSchema) -> UserModel:
        try:
            if await self.auth_repository.user_exists_by_email(user_data.email):
                CoffeeAppHttpResponse.bad_request(
                    data=None,
                    error_id=CoffeeAppResponseCodes.EXISTING_EMAIL.code,
                    message=CoffeeAppResponseCodes.EXISTING_EMAIL.detail,
                )

            hashed_password = get_password_hash(user_data.password)
            
            user_dict = {
                "role": UserRoles.CUSTOMER.value,
                "name": user_data.name,
                "last_name": user_data.last_name,
                "birth_date": user_data.birth_date,
                "email": user_data.email,
                "password": hashed_password,
                "points": 0.0,
                "is_verified": False
            }

            user = await self.auth_repository.create_user(user_dict)
            return user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def authenticate_user(self, email: EmailStr, password: str) -> UserModel:
        try:
            user = await self.auth_repository.get_user_by_email(email)
            
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            if not verify_password(password, user.password):
                CoffeeAppHttpResponse.unauthorized_with_code(
                    error_id=CoffeeAppResponseCodes.INVALID_PASSWORD.code,
                    message=CoffeeAppResponseCodes.INVALID_PASSWORD.detail,
                )
            
            if not user.is_verified:
                CoffeeAppHttpResponse.forbidden(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNVERIFIED_USER.code,
                    message=CoffeeAppResponseCodes.UNVERIFIED_USER.detail,
                )
            
            return user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    def generate_tokens_for_user(self, user: UserModel) -> dict:
        access_token = get_user_token(user, is_refresh=False)
        refresh_token = get_user_token(user, is_refresh=True)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    async def verify_user_account(self, user_id: UUID) -> dict:
        """
        Verificar cuenta de usuario
        """
        try:
            # Solo usuarios existentes pueden ser verificados
            user = await self.auth_repository.get_user_by_id(user_id)
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            # No verificar usuarios ya verificados
            if user.is_verified:
                return {"message": "User already verified"}
            
            await self.auth_repository.update_user_verification(user_id, True)
            
            return {"message": "User verified successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def reset_user_password(self, user_id: UUID, new_password: str) -> dict:
        """
        Reset de contraseña (por email/token)
        """
        try:
            # Usuario debe existir
            user = await self.auth_repository.get_user_by_id(user_id)
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            hashed_password = get_password_hash(new_password)
            
            await self.auth_repository.update_user_password(user_id, hashed_password)
            
            return {"message": "Password reset successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

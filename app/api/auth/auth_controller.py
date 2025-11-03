from sqlmodel import Session
from fastapi import HTTPException
from pydantic import EmailStr

from app.core.http_response import CoffeeAppHttpResponse
from app.constants.response_codes import CoffeeAppResponseCodes
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema
from app.api.auth.auth_service import AuthService
from app.utils.email import EmailService

class AuthController:
    def __init__(self, session: Session):
        self.auth_service = AuthService(session)

    async def signup(self, data: SignupSchema) -> AuthResponseSchema:
        """
        Registro de usuario con generación y envío de código de verificación
        """
        try:
            # Crear usuario (incluye validación de email existente)
            user = await self.auth_service.signup_user(data)
            
            # Generar y crear código de verificación
            verification_code = await self.auth_service.generate_and_create_verification_code(user.user_id)
            
            # Enviar email con código de verificación
            await EmailService.send_verification_email(
                to_name=user.name.capitalize(),
                to_email=user.email,
                verification_code=verification_code.code,
            )
            
            # Generar tokens
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
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def login(self, email: EmailStr, password: str) -> AuthResponseSchema:
        """
        Inicio de sesión de usuario
        """
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
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def verify_verification_code(self, code: str) -> dict:
        """
        Verificar código de verificación y activar cuenta de usuario
        """
        try:
            result = await self.auth_service.verify_user_with_code(code)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def resend_verification_code(self, email: EmailStr) -> dict:
        """
        Reenviar código de verificación al email del usuario
        """
        try:
            result = await self.auth_service.resend_verification_code(email)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()


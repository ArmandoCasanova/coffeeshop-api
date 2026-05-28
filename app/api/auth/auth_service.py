from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session
from fastapi import HTTPException, Response, status
from pydantic import EmailStr
from typing import Union

from app.models.users.user_model import UserModel
from app.models.users.verification_code_model import VerificationCodeModel
from app.models.users.verification_code_password_reset_model import VerificationCodePasswordResetModel
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
        self.session = session
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

    # ==================== VERIFICATION CODE METHODS ====================

    async def generate_and_create_verification_code(
        self, user_id: UUID, email: str = None
    ) -> VerificationCodeModel:
        """
        Generar y crear código de verificación único para un usuario.
        Si se pasa email y coincide con E2E_TEST_EMAIL, se usará el código fijo de testing.
        """
        try:
            code = await self.auth_repository.generate_unique_verification_code(
                is_password_reset=False, email=email
            )
            verification_code = await self.auth_repository.create_verification_code(code, user_id)
            
            return verification_code
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def generate_and_create_password_reset_code(
        self, user_id: UUID, email: str = None
    ) -> VerificationCodePasswordResetModel:
        """
        Generar (o actualizar) código de reset de contraseña para un usuario.
        Si se pasa email y coincide con E2E_TEST_EMAIL, se usará el código fijo de testing.
        """
        try:            

            code = await self.auth_repository.generate_unique_verification_code(
                is_password_reset=True, email=email
            )
            reset_code = await self.auth_repository.create_password_reset_code(code, user_id)          
            return reset_code

        except HTTPException:
            raise
        except Exception as e:            
            CoffeeAppHttpResponse.internal_error()


    async def get_and_validate_verification_code(self, code: str) -> VerificationCodeModel:
        """
        Obtener y validar código de verificación
        Aplica validaciones de negocio: existe, está activo
        """
        try:

            verification_code = await self.auth_repository.get_verification_code(code)
            
            if not verification_code:
  
                CoffeeAppHttpResponse.unauthorized_with_code(
                    error_id=CoffeeAppResponseCodes.INVALID_CODE.code,
                    message=CoffeeAppResponseCodes.INVALID_CODE.detail,
                )
            
            if not verification_code.is_alive:
              
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                        "providedValue": {"code": verification_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.ALREADY_USED_CODE.code,
                    message=CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                )
                
            now_utc = datetime.now(timezone.utc)
            
            if verification_code.expires_at.tzinfo is None:
                expires_at_aware = verification_code.expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at_aware = verification_code.expires_at

            if expires_at_aware < now_utc:
              
                await self.auth_repository.update_verification_code_status(
                    verification_code,
                    is_alive=False,
                )
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                        "providedValue": {"code": verification_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.EXPIRED_CODE.code,
                    message=CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                )
            
            return verification_code
        except HTTPException:
            raise
       

    async def get_and_validate_password_reset_code(self, code: str) -> VerificationCodePasswordResetModel:
        """
        Obtener y validar código de reset de contraseña
        """
        try:

            reset_code = await self.auth_repository.get_password_reset_code(code)
            
            if not reset_code:
                CoffeeAppHttpResponse.unauthorized_with_code(
                    error_id=CoffeeAppResponseCodes.INVALID_CODE.code,
                    message=CoffeeAppResponseCodes.INVALID_CODE.detail,
                )
            
            if not reset_code.is_alive:
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                        "providedValue": {"code": reset_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.ALREADY_USED_CODE.code,
                    message=CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                )

            now_utc = datetime.now(timezone.utc)
            
            if reset_code.is_alive.expires_at.tzinfo is None:
                expires_at_aware = reset_code.is_alive.expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at_aware = reset_code.is_alive.expires_at

            if expires_at_aware < now_utc:
            
                await self.auth_repository.update_verification_code_status(
                    reset_code,
                    is_alive=False,
                )
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                        "providedValue": {"code": reset_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.EXPIRED_CODE.code,
                    message=CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                )
            
            return reset_code
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def verify_user_with_code(self, code: str) -> dict:
        """
        Verificar usuario usando código de verificación
        Proceso completo: validar código, marcar como usado, verificar usuario
        """
        try:            
            # Validar y obtener código
            verification_code = await self.get_and_validate_verification_code(code)
            
            # Marcar código como usado
            await self.auth_repository.update_verification_code_status(verification_code, is_alive=False)
            
            # Verificar usuario
            await self.auth_repository.update_user_verification(verification_code.user_id, True)            
            
            return {"message": "User verified successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def validate_password_reset_code(self, code: str) -> UUID:
        """
        Validar código de reset de contraseña y retornar user_id
        Marca el código como usado
        """
        try:            
            # Validar y obtener código
            reset_code = await self.get_and_validate_password_reset_code(code)
            
            # Marcar código como usado
            await self.auth_repository.update_verification_code_status(reset_code, is_alive=False)
            
            return reset_code.user_id
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def resend_verification_code(self, email: EmailStr) -> dict:
        """
        Reenviar código de verificación a un usuario
        Genera nuevo código y envía por email
        """
        try:            
            # Verificar que el usuario existe
            user = await self.auth_repository.get_user_by_email(email)
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            # Verificar que el usuario no esté ya verificado
            if user.is_verified:
                return {"message": "User already verified"}
            
            # Generar nuevo código de verificación
            verification_code = await self.generate_and_create_verification_code(user.user_id)
            
            # Enviar email con el código (importar EmailService si no está)
            from app.utils.email import EmailService
            await EmailService.send_verification_email(
                to_name=user.name.capitalize(),
                to_email=user.email,
                verification_code=verification_code.code,
            )
            
            return {"message": "Verification code resent successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def logout_user(self, user_id: str) -> dict:
        """
        Cerrar sesión del usuario y limpiar cache de Redis
        """
        try:
            from app.core.redis_client import RedisClient
            
            # Limpiar cache de Redis para este usuario
            # Patrón para encontrar todas las keys del usuario (products, categories, etc.)
            await RedisClient.delete_pattern(f"*{user_id}*")
            
            return {"message": "Logout successful, cache cleared"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def verify_password_reset_code(self, code: str) -> dict:
        """
        Verificar usuario usando código de verificación
        Proceso completo: validar código, marcar como usado, verificar usuario
        """
        try:            
            # Validar y obtener código
            verification_code = await self.get_and_validate_password_reset_code(code)
            
            # Marcar código como usado
            await self.auth_repository.update_verification_code_status(verification_code, is_alive=False)
            
            return Response(status_code=status.HTTP_200_OK)
        
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def get_and_validate_password_reset_code(self, code: str) -> VerificationCodeModel:
        """
        Obtener y validar código de verificación
        Aplica validaciones de negocio: existe, está activo
        """
        try:            
            password_reset_code = await self.auth_repository.get_password_reset_code(code)
            
            if not password_reset_code:                
                CoffeeAppHttpResponse.unauthorized_with_code(
                    error_id=CoffeeAppResponseCodes.INVALID_CODE.code,
                    message=CoffeeAppResponseCodes.INVALID_CODE.detail,
                )
            
            if not password_reset_code.is_alive:                
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                        "providedValue": {"code": password_reset_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.ALREADY_USED_CODE.code,
                    message=CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                )


            now_utc = datetime.now(timezone.utc)
            
            if password_reset_code.expires_at.tzinfo is None:
                expires_at_aware = password_reset_code.expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at_aware = password_reset_code.expires_at

            if expires_at_aware < now_utc:             
                await self.auth_repository.update_verification_code_status(
                    password_reset_code,
                    is_alive=False,
                )
                CoffeeAppHttpResponse.bad_request(
                    data={
                        "message": CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                        "providedValue": {"code": password_reset_code.code},
                    },
                    error_id=CoffeeAppResponseCodes.EXPIRED_CODE.code,
                    message=CoffeeAppResponseCodes.EXPIRED_CODE.detail,
                )
            
            return password_reset_code
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_password(self, user_id: UUID, password: str):
        try:
            hashed_password = get_password_hash(password)
            await self.auth_repository.update_user_password(
                user_id=user_id,
                hashed_password=hashed_password
            )
        except Exception:
            CoffeeAppHttpResponse.internal_error()

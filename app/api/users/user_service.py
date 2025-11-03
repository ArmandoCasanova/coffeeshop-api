from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import Session
from fastapi import HTTPException

from app.models.users.user_model import UserModel
from app.api.users.user_repository import UserRepository
from app.api.users.user_schema import UserUpdateSchema
from app.constants.response_codes import CoffeeAppResponseCodes
from app.utils.security import get_password_hash, verify_password
from app.core.http_response import CoffeeAppHttpResponse


class UserService:
    """
    Servicio para gestión de usuarios (perfil).
    Maneja lógica de negocio y coordina con UserRepository.
    """
    
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    async def get_user_profile(self, user_id: UUID) -> UserModel:
        """Obtener perfil de usuario por ID con validaciones"""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            return user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_profile(self, user_id: UUID, user_data: UserUpdateSchema) -> UserModel:
        """Actualizar perfil de usuario con validaciones"""
        try:
            # Validar que el usuario existe
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            # Preparar datos para actualización
            update_data = user_data.model_dump(exclude_unset=True)
            
            # Actualizar usuario
            updated_user = await self.user_repository.update_user_profile(user_id, update_data)
            return updated_user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def change_user_password(self, user_id: UUID, old_password: str, new_password: str) -> dict:
        """Cambiar contraseña de usuario (requiere contraseña actual)"""
        try:
            # Obtener usuario
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                CoffeeAppHttpResponse.not_found(
                    data=None,
                    error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
                    message=CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                )
            
            # Verificar contraseña actual
            if not verify_password(old_password, user.password):
                CoffeeAppHttpResponse.unauthorized_with_code(
                    error_id=CoffeeAppResponseCodes.INVALID_PASSWORD.code,
                    message=CoffeeAppResponseCodes.INVALID_PASSWORD.detail,
                )
            
            # Hashear nueva contraseña
            hashed_password = get_password_hash(new_password)
            
            # Actualizar contraseña
            await self.user_repository.update_user_password(user_id, hashed_password)
            
            return {"message": "Password changed successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()


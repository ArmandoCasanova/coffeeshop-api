from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import Session
from fastapi import HTTPException
from sqlmodel import Session
from fastapi import HTTPException

from app.models.users.user_model import UserModel
from app.api.users.user_repository import UserRepository
from app.api.users.user_schema import UserResponseSchema, UserUpdateSchema
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
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": 404,
                        "statusMessage": "User does not exist",
                        "error": {"code": CoffeeAppResponseCodes.UNEXISTING_USER.code},
                    },
                )

            return user
        except HTTPException:
            raise
        except Exception as e:

            CoffeeAppHttpResponse.internal_error()

    async def update_user_profile(
        self, user_id: UUID, user_data: UserUpdateSchema
    ) -> UserModel:
        """Actualizar perfil de usuario con validaciones"""
        try:

            user = await self.user_repository.get_user_by_id(user_id)

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": 404,
                        "statusMessage": "User does not exist",
                        "error": {"code": CoffeeAppResponseCodes.UNEXISTING_USER.code},
                    },
                )

            update_data = user_data.model_dump(exclude_unset=True)

            updated_user = await self.user_repository.update_user_profile(
                user_id, update_data
            )

            return UserResponseSchema.from_orm(updated_user)
        except HTTPException:
            raise
        except Exception as e:

            CoffeeAppHttpResponse.internal_error()

    async def change_user_password(
        self, user_id: UUID, old_password: str, new_password: str
    ) -> dict:

        try:

            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": 404,
                        "statusMessage": "User does not exist",
                        "error": {"code": CoffeeAppResponseCodes.UNEXISTING_USER.code},
                    },
                )

            if not verify_password(old_password, user.password):
                raise HTTPException(
                    status_code=401,
                    detail={
                        "status": 401,
                        "statusMessage": "Invalid password",
                        "error": {"code": CoffeeAppResponseCodes.INVALID_PASSWORD.code},
                    },
                )

            hashed_password = get_password_hash(new_password)

            await self.user_repository.update_user_password(user_id, hashed_password)

            return {"message": "Password changed successfully"}
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

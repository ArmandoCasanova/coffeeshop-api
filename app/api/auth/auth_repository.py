from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException
from pydantic import EmailStr

from app.models.users.user_model import UserModel
from app.utils.security import get_password_hash
from app.core.http_response import CoffeeAppHttpResponse


class AuthRepository:
    """
    Repository para acceso a datos relacionados con autenticación.
    Solo contiene operaciones CRUD, sin lógica de negocio.
    """
    
    def __init__(self, session: Session):
        self.session = session

    async def get_user_by_email(self, email: EmailStr) -> UserModel | None:
        """Buscar usuario por email - Solo acceso a datos"""
        try:
            statement = select(UserModel).where(UserModel.email == email)
            user = self.session.exec(statement).first()
            return user
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def create_user(self, user_data: dict) -> UserModel:
        """Crear nuevo usuario en la BD - Solo acceso a datos"""
        try:
            new_user = UserModel(**user_data)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def get_user_by_id(self, user_id: UUID) -> UserModel | None:
        """Obtener usuario por ID - Solo acceso a datos"""
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = self.session.exec(statement).first()
            return user
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_verification(self, user_id: UUID, is_verified: bool = True) -> None:
        """Actualizar estado de verificación del usuario"""
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = self.session.exec(statement).first()
            if user:
                user.is_verified = is_verified
                user.updated_at = datetime.now(timezone.utc)
                self.session.add(user)
                self.session.commit()
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_password(self, user_id: UUID, hashed_password: str) -> None:
        """Actualizar contraseña hasheada del usuario"""
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = self.session.exec(statement).first()
            if user:
                user.password = hashed_password
                user.updated_at = datetime.now(timezone.utc)
                self.session.add(user)
                self.session.commit()
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def user_exists_by_email(self, email: EmailStr) -> bool:
        """Verificar si existe un usuario con ese email"""
        try:
            statement = select(UserModel).where(UserModel.email == email)
            user = self.session.exec(statement).first()
            return user is not None
        except Exception:
            CoffeeAppHttpResponse.internal_error()

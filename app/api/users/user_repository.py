from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.users.user_model import UserModel
from app.utils.security import get_password_hash
from app.core.http_response import CoffeeAppHttpResponse

class UserRepository:
    """
    Repository para acceso a datos de usuarios (gestión de perfil).
    Solo contiene operaciones CRUD, sin lógica de negocio.
    """
    
    def __init__(self, session: Session):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> UserModel | None:
        """Obtener usuario por ID - Solo acceso a datos"""
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = self.session.exec(statement).first()
            return user
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_profile(self, user_id: UUID, update_data: dict) -> UserModel:
        """Actualizar datos del perfil del usuario - Solo acceso a datos"""
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = self.session.exec(statement).first()
            
            if not user:
                raise ValueError("User not found")
            
            # Actualizar campos proporcionados
            for field, value in update_data.items():
                if hasattr(user, field) and value is not None:
                    setattr(user, field, value)
            
            user.updated_at = datetime.now(timezone.utc)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except ValueError:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_user_password(self, user_id: UUID, hashed_password: str) -> None:
        """Actualizar contraseña hasheada - Solo acceso a datos"""
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

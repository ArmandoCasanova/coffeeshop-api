from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException
from pydantic import EmailStr
from random import randint
from typing import Union, Optional

from app.models.users.user_model import UserModel
from app.models.users.verification_code_model import VerificationCodeModel
from app.models.users.verification_code_password_reset_model import VerificationCodePasswordResetModel
from app.utils.security import get_password_hash
from app.core.http_response import CoffeeAppHttpResponse
from app.core.settings import settings


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

    # ==================== VERIFICATION CODE METHODS ====================
    
    async def generate_unique_verification_code(
        self,
        is_password_reset: bool = False,
        email: Optional[str] = None,
    ) -> str:
        """
        Generar código único de 4 dígitos.
        Si el email coincide con E2E_TEST_EMAIL (variable de entorno),
        retorna E2E_TEST_VERIFICATION_CODE directamente para facilitar tests E2E.
        Args:
            is_password_reset: Si True, verifica en tabla de password reset, si False en verification codes
            email: Email del usuario (opcional). Si coincide con E2E_TEST_EMAIL, retorna código fijo.
        """
        try:
            # --- E2E Testing bypass ---
            if (
                settings.E2E_TEST_EMAIL
                and email
                and email.lower() == settings.E2E_TEST_EMAIL.lower()
            ):
                return settings.E2E_TEST_VERIFICATION_CODE
            # --------------------------

            model = VerificationCodePasswordResetModel if is_password_reset else VerificationCodeModel
        
            while True:
                code_digits = [randint(0, 9) for _ in range(4)]
                code = "".join(map(str, code_digits))
                
                statement = select(model).where(model.code == code)
                existing_code = self.session.exec(statement).first()
                
                if not existing_code:
                    return code
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def create_verification_code(self, code: str, user_id: UUID) -> VerificationCodeModel:
        """Crear nuevo código de verificación"""
        try:
            new_code = VerificationCodeModel(code=code, user_id=user_id)
            self.session.add(new_code)
            self.session.commit()
            self.session.refresh(new_code)
            return new_code
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def create_password_reset_code(self, code: str, user_id: UUID) -> VerificationCodePasswordResetModel:
        """
        Crear o actualizar código de reset de contraseña para un usuario.
        Si ya existe un registro previo, se actualiza con un nuevo código.
        """
        try:            
            statement = select(VerificationCodePasswordResetModel).where(
                VerificationCodePasswordResetModel.user_id == user_id
            )
            existing_code = self.session.exec(statement).first()

            if existing_code:                
                existing_code.code = code
                existing_code.is_alive = True
                existing_code.updated_at = datetime.now(timezone.utc)
                self.session.add(existing_code)
                self.session.commit()
                self.session.refresh(existing_code)
                return existing_code
            
            new_code = VerificationCodePasswordResetModel(
                code=code,
                user_id=user_id,
                is_alive=True,
                created_at=datetime.now(timezone.utc),
            )
            self.session.add(new_code)
            self.session.commit()
            self.session.refresh(new_code)            
            return new_code

        except Exception as e:            
            CoffeeAppHttpResponse.internal_error()

    async def get_verification_code(self, code: str) -> VerificationCodeModel | None:
        """Obtener código de verificación por código"""
        try:
            statement = select(VerificationCodeModel).where(VerificationCodeModel.code == code)
            return self.session.exec(statement).first()
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def get_password_reset_code(self, code: str) -> VerificationCodePasswordResetModel | None:
        """Obtener código de reset de contraseña por código"""
        try:
            statement = select(VerificationCodePasswordResetModel).where(
                VerificationCodePasswordResetModel.code == code
            )
            return self.session.exec(statement).first()
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def update_verification_code_status(
        self, 
        verification_code: Union[VerificationCodeModel, VerificationCodePasswordResetModel],
        is_alive: bool = False
    ) -> None:
        """Actualizar estado del código de verificación"""
        try:
            verification_code.is_alive = is_alive
            self.session.add(verification_code)
            self.session.commit()
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def get_password_reset_code(self, code: str) -> VerificationCodePasswordResetModel | None:
        """Obtener código de verificación por código"""
        try:
            statement = select(VerificationCodePasswordResetModel).where(VerificationCodePasswordResetModel.code == code)
            return self.session.exec(statement).first()
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
from uuid import UUID
from datetime import datetime, timezone

from sqlmodel import Session, select
from random import choice, randint
from typing import Union

from app.models.users.user_model import UserModel
from app.models.users.verification_code_model import VerificationCodeModel
from app.models.users.verification_code_password_reset_model import VerificationCodePasswordResetModel
from .user_schema import UserCreateSchema

from app.constants.user_constants import VerificationModels
from app.utils.security import get_password_hash
from app.core.http_response import CoffeeAppHttpResponse


class UserService:
    @staticmethod
    async def create_user(
        user_data: UserCreateSchema, role: str, session: Session
    ) -> UserModel:
        try:
            hashed_password = get_password_hash(user_data.password)
            user_dump = user_data.model_dump()
            new_user = UserModel(
                role=role,
                name=user_dump["name"],
                last_name=user_dump["last_name"],
                birth_date=user_dump.get("birth_date"),
                email=user_dump["email"],
                password=hashed_password,
                points=user_dump.get("points", 0.0),
                is_verified=user_dump.get("is_verified", False)
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def get_user_by_id(user_id: UUID, session: Session) -> UserModel:
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = session.exec(statement).first()
            return user
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def get_user_by_email(email: str, session: Session) -> UserModel | bool:
        try:
            statement = select(UserModel).where(UserModel.email == email)
            user = session.exec(statement).first()
            return user if user else False
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def verify_user(user_id: UUID, session: Session):
        try:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = session.exec(statement).first()
            if user:
                user.is_verified = True
                user.updated_at = datetime.now(timezone.utc)
                session.add(user)
                session.commit()
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def update_user_password(user_id: UUID, password: str, session: Session):
        try:
            hashed_password = get_password_hash(password)
            statement = select(UserModel).where(UserModel.user_id == user_id)
            user = session.exec(statement).first()
            if user:
                user.password = hashed_password
                user.updated_at = datetime.now(timezone.utc)
                session.add(user)
                session.commit()
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    @staticmethod
    async def generate_unique_verification_code(
        session: Session, model: VerificationModels
    ) -> str:
        try:
            while True:
                code_digits = [randint(0, 9) for _ in range(4)]
                code = "".join(map(str, code_digits))
                if model == "VerificationCodeModel":
                    existing_code = session.exec(
                        select(VerificationCodeModel).where(
                            VerificationCodeModel.code == code
                        )
                    ).first()
                else:
                    existing_code = session.exec(
                        select(VerificationCodePasswordResetModel).where(
                            VerificationCodePasswordResetModel.code == code
                        )
                    ).first()

                if not existing_code:
                    return code
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    @staticmethod
    async def create_verification_code(
        code: str,
        user_id: UUID,
        session: Session,
    ) -> VerificationCodeModel:
        try:
            new_code = VerificationCodeModel(code=code, user_id=user_id)

            session.add(new_code)
            session.commit()
            session.refresh(new_code)

            return new_code
        except Exception:
           CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def get_verification_code(
        code: str, table: VerificationModels, session: Session
    ) -> VerificationCodeModel:
        try:
            if table == VerificationModels.VERIFICATION_CODE_MODEL:
                statement = select(VerificationCodeModel).where(
                    VerificationCodeModel.code == code
                )
                result = session.exec(statement).first()
            else:
                statement = select(VerificationCodePasswordResetModel).where(
                    VerificationCodePasswordResetModel.code == code
                )

                result = session.exec(statement).first()

            return result
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    @staticmethod
    async def update_verification_code_status(
        verification_code: Union[VerificationCodeModel],
        session: Session,
    ):
        try:
            if isinstance(verification_code, VerificationCodeModel):
                verification_code.is_alive = False
                session.add(verification_code)
                session.commit()
            else:
                verification_code.is_alive = False
                session.add(verification_code)
                session.commit()
        except Exception:
            CoffeeAppHttpResponse.internal_error()


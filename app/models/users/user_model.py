from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, Column, Enum
from app.core.base_model import BaseCoffeeAppModel
from datetime import datetime, date
from uuid import UUID, uuid4
import enum

if TYPE_CHECKING:
    from .user_qr_code_model import UserQRCodeModel
    from .verification_code_model import VerificationCodeModel
    from .verification_code_password_reset_model import VerificationCodePasswordResetModel

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"

class UserModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "users"

    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: UserRole = Field(default=UserRole.customer, sa_column=Column(Enum(UserRole), nullable=False))
    name: str
    last_name: str
    birth_date: Optional[date] = Field(default=None)
    email: str = Field(index=True, unique=True)
    password: str
    points: float = Field(default=0.0)
    is_verified: bool = Field(default=False)
    
    # OAuth Fields
    oauth_provider: Optional[str] = Field(default=None, index=True)  # google, github, etc.
    oauth_provider_id: Optional[str] = Field(default=None, index=True)  # ID externo del proveedor
    oauth_email_verified: bool = Field(default=False)  # Si el email fue verificado por el proveedor OAuth
    picture_url: Optional[str] = Field(default=None)  # URL de la foto de perfil

    qr_codes: List["UserQRCodeModel"] = Relationship(back_populates="user")
    verification_codes: List["VerificationCodeModel"] = Relationship(back_populates="user")
    verification_codes_password_reset: List["VerificationCodePasswordResetModel"] = Relationship(back_populates="user")

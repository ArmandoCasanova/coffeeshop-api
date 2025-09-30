from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .user_qr_code_model import UserQRCodeModel
    from .verification_code_model import VerificationCodeModel
    from .verification_code_password_reset_model import VerificationCodePasswordResetModel

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"

class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    rol: UserRole = Field(sa_column=Column(Enum(UserRole), nullable=False))
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    points: float = Field(default=0.0)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    qr_codes: List["UserQRCodeModel"] = Relationship(back_populates="user")
    verification_codes: List["VerificationCodeModel"] = Relationship(back_populates="user")
    verification_codes_password_reset: List["VerificationCodePasswordResetModel"] = Relationship(back_populates="user")

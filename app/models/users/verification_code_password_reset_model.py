from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_model import UserModel

class VerificationCodePasswordResetModel(SQLModel, table=True):
    __tablename__ = "verification_codes_password_reset"

    verification_code_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    code: str
    is_alive: bool = Field(default=True)

    user: "UserModel" = Relationship(back_populates="verification_codes_password_reset")

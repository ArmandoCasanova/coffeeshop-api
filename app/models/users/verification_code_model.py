from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone

if TYPE_CHECKING:
    from .user_model import UserModel

class VerificationCodeModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "verification_codes"

    verification_code_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    code: str
    is_alive: bool = Field(default=True)

    user: "UserModel" = Relationship(back_populates="verification_codes")

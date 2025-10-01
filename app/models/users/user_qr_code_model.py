from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.core.base_model import BaseCoffeeAppModel
from datetime import datetime

if TYPE_CHECKING:
    from .user_model import UserModel

class UserQRCodeModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "user_qr_codes"

    qr_code_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    qr_code_string: str
    is_alive: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "UserModel" = Relationship(back_populates="qr_codes")

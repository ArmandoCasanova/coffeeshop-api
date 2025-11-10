from typing import Optional
from sqlmodel import Field, Column, Enum
from app.core.base_model import BaseCoffeeAppModel
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import UUID, uuid4
import enum


class NotificationType(str, enum.Enum):
    payment_successful = "payment_successful"
    payment_failed = "payment_failed"
    promotion = "promotion"
    points = "points"


class NotificationModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "notifications"
    notification_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.user_id", index=True)
    type: NotificationType = Field(sa_column=Column(Enum(NotificationType), nullable=False))
    subtype: Optional[str] = None
    title: str
    body: Optional[str] = None
    data: dict = Field(sa_column=Column(JSONB), default={})
    is_read: bool = Field(default=False)
    expires_at: Optional[datetime] = None

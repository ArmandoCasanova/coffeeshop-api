from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from pydantic.alias_generators import to_camel


class NotificationCreateSchema(BaseModel):
    user_id: Optional[UUID] = None
    type: str
    subtype: Optional[str] = None
    title: str
    body: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}
    expires_at: Optional[datetime] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class NotificationResponseSchema(BaseModel):
    notification_id: UUID
    user_id: Optional[UUID] = None
    type: str
    subtype: Optional[str] = None
    title: str
    body: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}
    is_read: bool
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponseSchema]
    total: int
    page: int
    page_size: int

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class MarkReadSchema(BaseModel):
    ids: List[UUID]

    class Config:
        alias_generator = to_camel
        populate_by_name = True

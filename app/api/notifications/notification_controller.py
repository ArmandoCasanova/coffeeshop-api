from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID

from app.api.notifications.notification_service import NotificationService
from app.api.notifications.notification_schema import (
    NotificationCreateSchema,
)


class NotificationController:
    def __init__(self, session: Session):
        self.service = NotificationService(session)

    async def create_notification(self, notification_data: NotificationCreateSchema):
        try:
            notif = await self.service.create_notification(notification_data.model_dump())
            return notif
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def get_notifications(self, user_id: UUID, page: int = 1, page_size: int = 10):
        try:
            skip = (page - 1) * page_size
            notifs, total = await self.service.get_notifications_for_user(user_id, skip, page_size)
            return notifs, total
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_read(self, ids: list, user_id: UUID):
        try:
            return await self.service.mark_read(ids, user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_all_read(self, user_id: UUID):
        try:
            return await self.service.mark_all_read(user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def delete_notification(self, notification_id: UUID, user_id: UUID):
        try:
            return await self.service.delete_notification(notification_id, user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

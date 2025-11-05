from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional, List, Tuple
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.notifications.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, session: Session):
        self.repo = NotificationRepository(session)

    async def create_notification(self, notification_data: dict):
        try:
            return await self.repo.create_notification(notification_data)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def get_notifications_for_user(self, user_id: UUID, skip: int = 0, limit: int = 10) -> Tuple[List, int]:
        try:
            return await self.repo.get_notifications_by_user(user_id, skip, limit)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_read(self, ids: list, user_id: UUID) -> int:
        try:
            return await self.repo.mark_read(ids, user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_all_read(self, user_id: UUID) -> int:
        try:
            return await self.repo.mark_all_read(user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def delete_notification(self, notification_id: UUID, user_id: UUID) -> bool:
        try:
            return await self.repo.delete_notification(notification_id, user_id)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

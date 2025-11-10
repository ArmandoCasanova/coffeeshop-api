from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID

from app.api.notifications.notification_service import NotificationService
from app.api.notifications.notification_schema import (
    NotificationCreateSchema,
    NotificationResponseSchema,
    NotificationListResponse,
)


class NotificationController:
    def __init__(self, session: Session):
        self.service = NotificationService(session)

    async def create_notification(self, notification_data: NotificationCreateSchema):
        """Create a notification (admin only)"""
        try:
            notif = await self.service.create_notification(notification_data.model_dump())
            return NotificationResponseSchema.model_validate(notif)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def get_notifications(self, user_id: UUID, page: int = 1, page_size: int = 10):
        """Get paginated notifications for a user"""
        try:
            skip = (page - 1) * page_size
            notifs, total = await self.service.get_notifications_for_user(user_id, skip, page_size)
            
            # Convert models to response schemas (using model_dump for safety)
            notif_list = [
                NotificationResponseSchema.model_validate(n.model_dump()) 
                for n in notifs
            ]
            
            return NotificationListResponse(
                notifications=notif_list,
                total=total,
                page=page,
                page_size=page_size
            )
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_read(self, ids: list, user_id: UUID):
        """Mark notifications as read"""
        try:
            count = await self.service.mark_read(ids, user_id)
            return {"updated": count}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_all_read(self, user_id: UUID):
        """Mark all notifications as read"""
        try:
            count = await self.service.mark_all_read(user_id)
            return {"updated": count}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def delete_notification(self, notification_id: UUID, user_id: UUID):
        """Delete a notification"""
        try:
            deleted = await self.service.delete_notification(notification_id, user_id)
            if not deleted:
                CoffeeAppHttpResponse.not_found(message="Notification not found")
            return {"message": "Notification deleted successfully"}
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

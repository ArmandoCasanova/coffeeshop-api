from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional, List, Tuple
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from app.api.notifications.notification_repository import NotificationRepository
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, session: Session):
        self.repo = NotificationRepository(session)
        self.session = session

    async def create_notification(self, notification_data: dict):
        """Create a notification with transaction control"""
        try:
            notif = await self.repo.create_notification(notification_data)
            self.session.commit()
            self.session.refresh(notif)
            return notif
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating notification: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def create_notification_safe(
        self, 
        user_id: UUID, 
        notification_type: str,
        title: str,
        body: str,
        data: dict = None
    ) -> bool:
        """
        Create a notification with error handling that doesn't break caller flow.
        Returns True if successful, False otherwise.
        This is designed for background/async notification creation from business events.
        """
        try:
            notification_data = {
                "user_id": user_id,
                "type": notification_type,
                "title": title,
                "body": body,
                "data": data or {},
            }
            await self.create_notification(notification_data)
            logger.info(f"Notification created successfully for user {user_id}: {notification_type}")
            return True
        except Exception as e:
            # Log but don't raise - notification failure should not break business flow
            logger.error(f"Failed to create notification for user {user_id}: {str(e)}", exc_info=True)
            return False

    async def get_notifications_for_user(self, user_id: UUID, skip: int = 0, limit: int = 10) -> Tuple[List, int]:
        try:
            return await self.repo.get_notifications_by_user(user_id, skip, limit)
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def mark_read(self, ids: list, user_id: UUID) -> int:
        """Mark notifications as read with transaction control"""
        try:
            count = await self.repo.mark_read(ids, user_id)
            self.session.commit()
            return count
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error marking notifications as read: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def mark_all_read(self, user_id: UUID) -> int:
        """Mark all notifications as read with transaction control"""
        try:
            count = await self.repo.mark_all_read(user_id)
            self.session.commit()
            return count
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error marking all notifications as read: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

    async def delete_notification(self, notification_id: UUID, user_id: UUID) -> bool:
        """Delete a notification with transaction control"""
        try:
            deleted = await self.repo.delete_notification(notification_id, user_id)
            if deleted:
                self.session.commit()
            return deleted
        except HTTPException:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting notification: {str(e)}")
            CoffeeAppHttpResponse.internal_error()

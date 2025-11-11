from typing import Optional, List, Tuple
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from app.models.notifications.notification_model import NotificationModel


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_notification(self, notification_data: dict) -> NotificationModel:
        """
        Create a notification record.
        Note: Does NOT commit - caller is responsible for commit/rollback.
        """
        try:
            new_notif = NotificationModel(**notification_data)
            self.session.add(new_notif)
            # No commit here - let the service/caller handle transaction
            return new_notif
        except Exception:
            raise

    async def get_notifications_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> Tuple[List[NotificationModel], int]:
        try:
            from sqlmodel import select
            from sqlalchemy import func

            statement = select(NotificationModel).where(NotificationModel.user_id == user_id).order_by(NotificationModel.created_at.desc())
            total_query = select(func.count(NotificationModel.notification_id)).where(NotificationModel.user_id == user_id)
            total = self.session.exec(total_query).one()
            results = self.session.exec(statement.offset(skip).limit(limit)).all()
            return results, total
        except Exception:
            raise

    async def mark_read(self, ids: list, user_id: UUID) -> int:
        """Mark notifications as read. Does NOT commit."""
        try:
            statement = select(NotificationModel).where(
                NotificationModel.notification_id.in_(ids), 
                NotificationModel.user_id == user_id
            )
            notifs = self.session.exec(statement).all()
            for n in notifs:
                n.is_read = True
                self.session.add(n)
            # No commit - let service handle it
            return len(notifs)
        except Exception:
            raise

    async def mark_all_read(self, user_id: UUID) -> int:
        """Mark all user notifications as read. Does NOT commit."""
        try:
            statement = select(NotificationModel).where(
                NotificationModel.user_id == user_id, 
                NotificationModel.is_read == False
            )
            notifs = self.session.exec(statement).all()
            for n in notifs:
                n.is_read = True
                self.session.add(n)
            # No commit - let service handle it
            return len(notifs)
        except Exception:
            raise

    async def delete_notification(self, notification_id: UUID, user_id: UUID) -> bool:
        """Delete a notification. Does NOT commit."""
        try:
            statement = select(NotificationModel).where(
                NotificationModel.notification_id == notification_id, 
                NotificationModel.user_id == user_id
            )
            notif = self.session.exec(statement).first()
            if not notif:
                return False
            self.session.delete(notif)
            # No commit - let service handle it
            return True
        except Exception:
            raise

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user
from app.models.users.user_model import UserModel, UserRole
from app.api.notifications.notification_controller import NotificationController
from app.api.notifications.notification_schema import (
    NotificationCreateSchema,
    NotificationResponseSchema,
    NotificationListResponse,
    MarkReadSchema,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=NotificationListResponse)
async def list_notifications(
    page: int = 1,
    page_size: int = 10,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    controller = NotificationController(session)
    notifs, total = await controller.get_notifications(current_user.user_id, page, page_size)
    notif_list = [NotificationResponseSchema.model_validate(n) for n in notifs]
    return NotificationListResponse(notifications=notif_list, total=total, page=page, page_size=page_size)


@router.post("/", response_model=NotificationResponseSchema)
async def create_notification(
    notification_data: NotificationCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Only admin can create arbitrary notifications
    if str(current_user.role) != "UserRole.admin" and getattr(current_user, 'role', None) != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can create notifications")
    controller = NotificationController(session)
    notif = await controller.create_notification(notification_data)
    return NotificationResponseSchema.model_validate(notif)


@router.post("/mark-read")
async def mark_read(
    payload: MarkReadSchema,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    controller = NotificationController(session)
    updated = await controller.mark_read(payload.ids, current_user.user_id)
    return {"updated": updated}


@router.post("/mark-all-read")
async def mark_all_read(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    controller = NotificationController(session)
    updated = await controller.mark_all_read(current_user.user_id)
    return {"updated": updated}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: UUID,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    controller = NotificationController(session)
    deleted = await controller.delete_notification(notification_id, current_user.user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted"}

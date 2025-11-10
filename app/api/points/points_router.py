from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user, admin_required
from app.models.users.user_model import UserModel
from app.api.points.points_controller import PointsController
from app.api.points.points_schema import (
    PointsConfigCreateSchema,
    PointsConfigUpdateSchema,
    PointsConfigResponseSchema,
)

router = APIRouter(prefix="/points", tags=["Points"])


@router.get("/config", response_model=PointsConfigResponseSchema)
async def get_active_config(
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get active points configuration (available to all authenticated users)"""
    controller = PointsController(session)
    return await controller.get_active_config()


@router.get("/config/all", response_model=list[PointsConfigResponseSchema])
async def get_all_configs(
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(admin_required)
):
    """Get all points configurations (admin only)"""
    controller = PointsController(session)
    return await controller.get_all_configs()


@router.post("/config", response_model=PointsConfigResponseSchema)
async def create_config(
    data: PointsConfigCreateSchema,
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(admin_required)
):
    """Create new points configuration (admin only)"""
    controller = PointsController(session)
    return await controller.create_config(data)


@router.put("/config/{config_id}", response_model=PointsConfigResponseSchema)
async def update_config(
    config_id: UUID,
    data: PointsConfigUpdateSchema,
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(admin_required)
):
    """Update points configuration (admin only)"""
    controller = PointsController(session)
    return await controller.update_config(config_id, data)

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user
from app.models.users.user_model import UserModel
from app.api.users.user_controller import UserController
from app.api.users.user_schema import (
    UserResponseSchema,
    UserUpdateSchema,
    UserPointsResponseSchema,
    ChangePasswordSchema
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/profile", response_model=UserResponseSchema)
async def get_user_profile(
    user_id: UUID, 
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Obtener perfil de usuario por ID"""
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied: can only access own profile")
    controller = UserController(session)
    return await controller.get_user_profile(user_id)


@router.put("/{user_id}/profile", response_model=UserResponseSchema)
async def update_user_profile(
    user_id: UUID,
    user_data: UserUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Actualizar perfil de usuario"""
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied: can only update own profile")
    controller = UserController(session)
    return await controller.update_user_profile(user_id, user_data)


@router.get("/{user_id}/points", response_model=UserPointsResponseSchema)
async def get_user_points(
    user_id: UUID,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Obtener puntos del usuario"""
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied: can only access own points")
    controller = UserController(session)
    return await controller.get_user_points(user_id)


@router.post("/{user_id}/change-password")
async def change_user_password(
    user_id: UUID,
    password_data: ChangePasswordSchema,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario"""
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied: can only change own password")
    controller = UserController(session)
    return await controller.change_user_password(
        user_id, 
        password_data.current_password, 
        password_data.new_password
    )
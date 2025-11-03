from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from app.core.database import get_db

from app.auth.auth_dependencies import get_current_user

from app.models.users.user_model import UserModel

from app.api.users.user_controller import UserController
from app.api.users.user_schema import (
    UserUpdateSchema,
    ChangePasswordSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/me", response_model=UserResponseSchema)
async def update_current_user_profile(
    data: UserUpdateSchema,
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    authorization: str | None = Header(default=None),
):

    try:
        controller = UserController(session)
        updated_user = await controller.update_user_profile(
            user_id=current_user.user_id, user_data=data
        )
        return updated_user

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/change-password")
async def change_current_user_password(
    data: ChangePasswordSchema,
    session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    authorization: str | None = Header(default=None),
):

    try:
        controller = UserController(session)
        await controller.change_user_password(
            user_id=current_user.user_id,
            old_password=data.current_password,
            new_password=data.new_password,
        )
    except HTTPException as e:

        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

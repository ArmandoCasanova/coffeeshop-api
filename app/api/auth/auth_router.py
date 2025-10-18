from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.auth import LoginFormDataDep
from app.core.database import SessionDep
from app.core.database import SessionDep, get_db
from app.api.auth.auth_controller import AuthController
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema, LoginSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponseSchema)
async def signup(data: SignupSchema, session: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    try:
        controller = AuthController(session)
        return await controller.signup(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin")
async def login(session: SessionDep, form_data: LoginFormDataDep):
    try:
        email = form_data.username
        password = form_data.password
        auth_controller = AuthController(session)

        current_user = await auth_controller.get_current_user_from_login(email=email)

        auth_controller.verify_user_password(user=current_user, password=password)

        await auth_controller.is_user_verified(user=current_user)

        return await auth_controller.login(user=current_user, password=password)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise e

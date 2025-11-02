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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin", response_model=AuthResponseSchema)
async def signin(data: LoginSchema, session: Session = Depends(get_db)):
    """Iniciar sesión"""
    try:
        controller = AuthController(session)
        return await controller.login(data.email, data.password)
    except Exception as e:
        raise e

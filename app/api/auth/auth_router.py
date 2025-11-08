from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.http_response import CoffeeAppHttpResponse
from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user
from app.models.users.user_model import UserModel
from app.api.auth.auth_controller import AuthController
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema, LoginSchema, VerificationRequest, ResendCode

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponseSchema)
async def signup(data: SignupSchema, session: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    try:
        controller = AuthController(session)
        return await controller.signup(data)
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()


@router.post("/signin", response_model=AuthResponseSchema)
async def signin(data: LoginSchema, session: Session = Depends(get_db)):
    """Iniciar sesión"""
    try:
        print("email"+ data.email)
        print("pass"+ data.password)
        controller = AuthController(session)
        return await controller.login(data.email, data.password)
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()


@router.post("/verification-code")
async def verify_user_verification_code(
    request: VerificationRequest, 
    session: Session = Depends(get_db)
):
    """Verificar código de verificación del usuario"""
    try:
        controller = AuthController(session)
        return await controller.verify_verification_code(request.code)
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()


@router.put("/resend-verification-code")
async def resend_verification_code(
    request: ResendCode,
    session: Session = Depends(get_db)
):
    """Reenviar código de verificación al usuario"""
    try:
        controller = AuthController(session)
        return await controller.resend_verification_code(request.email)
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()


@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Cerrar sesión y limpiar cache de Redis"""
    try:
        controller = AuthController(session)
        return await controller.logout(str(current_user.user_id))
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()


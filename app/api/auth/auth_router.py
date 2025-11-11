from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.http_response import CoffeeAppHttpResponse
from app.core.database import get_db
from app.auth.auth_dependencies import get_current_user
from app.models.users.user_model import UserModel
from app.api.auth.auth_controller import AuthController
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema, LoginSchema, VerificationRequest, ResendCode, RequestPasswordChange, ResetPasswordRequest

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


@router.post("/password-change-request")
async def request_password_reset_verification_code(
    request: RequestPasswordChange, session: Session = Depends(get_db)
):
    try:       
        auth_controller = AuthController(session=session)
        user_verified = await auth_controller.get_current_user(email=request.email)
      
        response = await auth_controller.request_password_reset_verification_code(
            user=user_verified
        )

        return response

    except HTTPException as e:
        raise e

    except Exception as e:
        raise e


@router.post("/verification-password-reset-code")
async def verify_verification_password_reset_code(
    request: VerificationRequest, 
    session: Session = Depends(get_db)
):  
    try:
        controller = AuthController(session)
        return await controller.verify_verification_password_reset_code(request.code)
    except HTTPException:
        raise
    except Exception:
        CoffeeAppHttpResponse.internal_error()

@router.put("/password-reset")
async def reset_password(request: ResetPasswordRequest, session: Session = Depends(get_db)):
    try:
        auth_controller = AuthController(session=session)

        user = await auth_controller.get_current_user(email=request.email)

        return await auth_controller.update_user_password(
            user_id=user.user_id, password=request.password
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise e



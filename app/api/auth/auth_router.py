from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.auth import LoginFormDataDep
from app.core.database import SessionDep, get_db
from app.api.auth.auth_controller import AuthController
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema, LoginSchema, VerificationRequest
from app.constants.user_constants import VerificationModels

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
        user = await controller.get_current_user_from_login(data.email)
        controller.verify_user_password(user, data.password)
        await controller.is_user_verified(user)
        return await controller.login(user, data.password)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    
@router.post("/verification-code")
async def verify_user_verification_code(
    request: VerificationRequest, session: SessionDep
):
    try:
        auth_controller = AuthController(session=session)

        verification_code = await auth_controller.get_verification_code_by_code(
            request=request, model=VerificationModels.VERIFICATION_CODE_MODEL
        )

        auth_controller.verify_is_code_alive(verification_code=verification_code)

        return await auth_controller.verify_code(
            verification_code_model=verification_code
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise e



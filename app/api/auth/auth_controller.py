from sqlmodel import Session
from fastapi import HTTPException, Response, BackgroundTasks
from pydantic import EmailStr
from uuid import UUID

from app.core.http_response import CoffeeAppHttpResponse
from app.constants.response_codes import CoffeeAppResponseCodes
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema
from app.api.auth.auth_service import AuthService
from app.utils.email import EmailService
from app.api.payments.payments_service import PaymentService
from app.models.users.user_model import UserModel
from app.api.users.user_service import UserService



class AuthController:
    def __init__(self, session: Session):
        self.session = session
        self.auth_service = AuthService(session)
        self.payment_service = PaymentService(session)
        self.user_service = UserService(session)

    async def signup(self, data: SignupSchema, background_tasks: BackgroundTasks) -> AuthResponseSchema:
        """
        Registro de usuario con generación y envío de código de verificación
        """
        try:
            # Crear usuario (incluye validación de email existente)
            user = await self.auth_service.signup_user(data)
            
            # Intentar crear Stripe customer (si falla, solo loguear el error)
            try:
                stripe_customer = self.payment_service.create_stripe_customer(user.user_id)
            except Exception as stripe_error:
                print(f"Error al crear Stripe customer: {stripe_error}")
                # Continuar con el signup aunque falle Stripe
            
            # Generar y crear código de verificación
            verification_code = await self.auth_service.generate_and_create_verification_code(
                user.user_id, email=user.email
            )
            
            # Enviar email con código de verificación EN BACKGROUND (no bloqueante)
            background_tasks.add_task(
                EmailService.send_verification_email,
                to_name=user.name.capitalize(),
                to_email=user.email,
                verification_code=verification_code.code,
            )
            
            # Generar tokens
            tokens = self.auth_service.generate_tokens_for_user(user)
            
            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                points=user.points,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()

    async def login(self, email: EmailStr, password: str) -> AuthResponseSchema:
        """
        Inicio de sesión de usuario
        """
        try:
            user = await self.auth_service.authenticate_user(email, password)
            tokens = self.auth_service.generate_tokens_for_user(user)
            
            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                points=user.points,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def verify_verification_code(self, code: str) -> dict:
        """
        Verificar código de verificación y activar cuenta de usuario
        """
        try:
            result = await self.auth_service.verify_user_with_code(code)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def resend_verification_code(self, email: EmailStr) -> dict:
        """
        Reenviar código de verificación al email del usuario
        """
        try:
            result = await self.auth_service.resend_verification_code(email)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def logout(self, user_id: str) -> dict:
        """
        Cerrar sesión del usuario y limpiar cache de Redis
        """
        try:
            result = await self.auth_service.logout_user(user_id)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
            
            
            
    
    async def get_current_user(self, email: str) -> UserModel:
        try:            
            user = await UserService.get_user_by_email(
            email=email, session=self.session
        )
            
            if user is False or user is None:                
                CoffeeAppHttpResponse.not_found(
                data={
                    "message": CoffeeAppResponseCodes.UNEXISTING_USER.detail,
                },
                error_id=CoffeeAppResponseCodes.UNEXISTING_USER.code,
            )      
                                  
            return user

        except HTTPException as e:            
            raise e

        except Exception as e:            
            CoffeeAppHttpResponse.internal_error()


    
    async def request_password_reset_verification_code(self, user: UserModel):       
        try:
            reset_code = await self.auth_service.generate_and_create_password_reset_code(
                user.user_id, email=user.email
            )

            EmailService.send_password_reset_code_email(
                to_name=user.name.capitalize(),
                to_email=user.email,
                verification_code=reset_code.code,
            )
        
            
            return Response(status_code=200)

        except HTTPException as e:
            raise e
        except Exception:
            CoffeeAppHttpResponse.internal_error()


    async def verify_verification_password_reset_code(self, code: str) -> dict:
        try:
            result = await self.auth_service.verify_password_reset_code(code)
            return result
        except HTTPException:
            raise
        except Exception:
            CoffeeAppHttpResponse.internal_error()
    
    async def update_user_password(self, user_id: UUID, password: str):
        try:            
            await self.auth_service.update_user_password(user_id=user_id, password=password)
            return Response(status_code=200)
        except HTTPException:
            CoffeeAppHttpResponse.internal_error()

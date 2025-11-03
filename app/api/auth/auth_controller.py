from sqlmodel import Session
from fastapi import HTTPException
from app.core.http_response import CoffeeAppHttpResponse
from pydantic import EmailStr
from app.constants.user_constants import UserRoles, VerificationModels
from app.models.users.user_model import UserModel
from app.api.users.user_service import UserService
from app.api.auth.auth_schema import SignupSchema, AuthResponseSchema, VerificationRequest
from app.models.users.verification_code_model import VerificationCodeModel
from app.utils.security import get_user_token, verify_password
from app.core.http_response import CoffeeAppHttpResponse
from app.constants.response_codes import CoffeeAppResponseCodes
from app.utils.email import EmailService
from typing import Union
from app.api.auth.auth_service import AuthService

class AuthController:
    def __init__(self, session: Session):
        self.auth_service = AuthService(session)

    async def signup(self, data: SignupSchema) -> AuthResponseSchema:
        try:
          
            existing_user = await UserService.get_user_by_email(
                data.email, self.session
            )
            if existing_user:
                CoffeeAppHttpResponse.bad_request(
                    data=None,
                    error_id=CoffeeAppResponseCodes.EXISTING_EMAIL.code,
                    message=CoffeeAppResponseCodes.EXISTING_EMAIL.detail,
                )

            user = await UserService.create_user(
                user_data=data, role=UserRoles.CUSTOMER.value, session=self.session
            )

            new_verification_code = await UserService.generate_unique_verification_code(
                session=self.session, model=VerificationModels.VERIFICATION_CODE_MODEL
            )

            verification_code = await UserService.create_verification_code(
                code=new_verification_code, user_id=user.user_id, session=self.session
            )

            await EmailService.send_verification_email(
                to_name=user.name.capitalize(),
                to_email=user.email,
                verification_code=verification_code.code,
            )
            
            access_token = get_user_token(user, is_refresh=False)
            refresh_token = get_user_token(user, is_refresh=True)

            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException as e:
            raise e

    async def login(self, email: EmailStr, password: str) -> AuthResponseSchema:
        try:
            user = await self.auth_service.authenticate_user(email, password)
            tokens = self.auth_service.generate_tokens_for_user(user)
            return AuthResponseSchema(
                user_id=user.user_id,
                email=user.email,
                name=user.name,
                last_name=user.last_name,
                role=user.role,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                is_verified=user.is_verified,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_verification_code_by_code(
        self, request: VerificationRequest, model=VerificationModels
    ):
        verification_code = await UserService.get_verification_code(
            code=request.code, table=model, session=self.session
        )

        if not verification_code:
            CoffeeAppHttpResponse.unauthorized_with_code(
                error_id=CoffeeAppResponseCodes.INVALID_CODE,
                message=CoffeeAppResponseCodes.INVALID_CODE,
            )

        return verification_code

    def verify_is_code_alive(self, verification_code: VerificationCodeModel) -> bool:
        if not verification_code.is_alive:
            CoffeeAppHttpResponse.bad_request(
                data={
                    "message": CoffeeAppResponseCodes.ALREADY_USED_CODE.detail,
                    "providedValue": {"code": verification_code.code},
                },
                error_id=CoffeeAppResponseCodes.ALREADY_USED_CODE.code,
            )

        return True
    
    async def verify_code(
        self,
        verification_code_model: Union[VerificationCodeModel],
    ):
        try:
            if isinstance(verification_code_model, VerificationCodeModel):
                user_id = verification_code_model.user_id

                await UserService.update_verification_code_status(
                    verification_code=verification_code_model, session=self.session
                )

                await UserService.verify_user(user_id=user_id, session=self.session)
            else:
                await UserService.update_verification_code_status(
                    verification_code=verification_code_model, session=self.session
                )

            return CoffeeAppHttpResponse.no_content()

        except HTTPException as e:
            raise e

        except Exception as e:
            CoffeeAppHttpResponse.internal_error()


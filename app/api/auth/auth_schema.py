
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel
from app.utils.regex import Regex

class SignupSchema(BaseModel):
    name: str = Field(min_length=4, max_length=20, pattern=Regex.USER_NAME)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(max_length=40)
    birth_date: datetime | None = None
    password: str = Field(min_length=8, max_length=20)

    class Config:
        extra = "forbid"
        alias_generator = to_camel
        populate_by_name = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class AuthResponseSchema(BaseModel):
    """Schema para respuestas de autenticación (login/signup)"""
    user_id: UUID
    email: EmailStr
    name: str
    last_name: str
    role: str
    points: float = 0.0
    access_token: str
    refresh_token: str
    is_verified: bool

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class TokenResponseSchema(BaseModel):
    """Schema para respuestas que solo contienen tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class VerificationRequest(BaseModel):
    code: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class RequestPasswordChange(BaseModel):
    email: EmailStr = Field(max_length=40)

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=8, max_length=50)

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class ResendCode(BaseModel):
    email: EmailStr = Field(max_length=40)

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class SelectProfileRequest(BaseModel):
    user_id: UUID
    id_animal: UUID

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class ConnectionCodeRequest(BaseModel):
    code: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class AdviceResponse(BaseModel):
    id: UUID
    title: str
    description: str

    model_config = {"from_attributes": True}
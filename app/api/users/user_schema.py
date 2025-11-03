from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel

from app.core.mixins.password_validation_mixin import PasswordValidationMixin

from app.utils.regex import Regex


from uuid import UUID

# user_schema.py
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import date


class UserResponseSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    last_name: str
    role: str = Field(..., alias="rol")
    birth_date: Optional[date] = None
    points: Optional[float] = 0.0
    is_verified: bool

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    user_id: UUID
    role: str = Field(..., alias="rol")
    name: str = Field(min_length=4, max_length=20, pattern=Regex.USER_NAME)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(max_length=40)
    birth_date: datetime | None = None
    points: float = 0.0
    is_verified: bool = False

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UserCreateSchema(UserSchema, PasswordValidationMixin):
    password: str

    class Config:
        extra = "forbid"


class UserResponseSchema(UserSchema):
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    name: str
    last_name: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True

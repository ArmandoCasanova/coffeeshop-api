from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel

from app.utils.regex import Regex
class UserSchema(BaseModel):
    user_id: UUID
    rol: str
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


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=4, max_length=20, pattern=Regex.USER_NAME)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(max_length=40)
    birth_date: datetime | None = None
    password: str = Field(min_length=8, max_length=20)
    confirm_password: str = Field(min_length=8, max_length=20)

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        extra = "forbid"


class UserResponseSchema(UserSchema):
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=4, max_length=20, pattern=Regex.USER_NAME)
    last_name: str | None = Field(None, min_length=2, max_length=30)
    email: EmailStr | None = Field(None, max_length=40)
    birth_date: datetime | None = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserPointsResponseSchema(BaseModel):
    user_id: UUID
    points: float

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(min_length=1, description="Contraseña actual del usuario")
    new_password: str = Field(min_length=8, max_length=20, description="Nueva contraseña")

    class Config:
        alias_generator = to_camel
        populate_by_name = True

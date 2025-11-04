from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic.alias_generators import to_camel

from app.utils.regex import Regex
class UserSchema(BaseModel):
    user_id: UUID
    role: str
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

    @field_validator("password")
    @classmethod
    def validate_password_fields(cls, p: str) -> str:
        import re
        re_for_pw: re.Pattern[str] = re.compile(Regex.PASSWORD)
        if not re_for_pw.match(p):
            raise ValueError("Contraseña no válida")
        return p

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreateSchema":
        if self.password != self.confirm_password:
            raise ValueError('Las contraseñas no coinciden')
        return self

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
    model_config = {"populate_by_name": True}
    
    current_password: str = Field(description="Contraseña actual del usuario", alias="currentPassword")
    new_password: str = Field(min_length=8, max_length=20, description="Nueva contraseña", alias="newPassword")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, password):
        import re
        re_for_pw: re.Pattern[str] = re.compile(Regex.PASSWORD)
        if not re_for_pw.match(password):
            raise ValueError("La contraseña debe contener al menos una letra minúscula, una mayúscula, un dígito y un carácter especial.")
        return password

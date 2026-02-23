from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID


class OAuthStartRequest(BaseModel):
    provider: str = Field(...)
    

class OAuthCallbackSchema(BaseModel):
    code: str = Field(...)
    state: str = Field(...)


class OAuthUserInfoSchema(BaseModel):
    provider: str
    provider_id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    email_verified: bool = False


class SessionSchema(BaseModel):
    session_id: str
    user_id: str
    created_at: str
    last_activity: str
    device_info: Optional[Dict[str, Any]] = None


class SessionResponseSchema(BaseModel):
    session_id: str
    user_id: UUID
    email: EmailStr
    name: str
    role: str
    token_type: str = "bearer"
    created_at: str


class UserOAuthResponseSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    last_name: str
    role: str
    points: float = 0.0
    oauth_provider: str
    access_token: str
    refresh_token: str
    session_id: str
    is_verified: bool

    class Config:
        from_attributes = True


class LogoutSchema(BaseModel):
    all_devices: bool = Field(False)


class SessionListSchema(BaseModel):
    total: int
    sessions: list[SessionSchema]


class MFASchema(BaseModel):
    code: str = Field(...)


class DeviceInfoSchema(BaseModel):
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    device_type: Optional[str] = None

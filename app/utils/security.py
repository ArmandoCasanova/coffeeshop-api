import jwt
import time
from uuid import UUID
from datetime import datetime, timezone, timedelta

from typing import Optional
from passlib.context import CryptContext

from app.core.settings import settings

from app.models.users.user_model import UserModel
from app.constants.user_constants import UserRoles

ACCESS_TOKEN_EXPIRY = 3600
REFRESH_TOKEN_EXPIRY = 7 * 24 * 3600

password_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expires_delta: timedelta = None, refresh_token: bool = False
) -> str:
    payload = {
        "sub": user_data["id"],
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "role": user_data["role"],
        },
        "exp": datetime.now(timezone.utc) + (
            expires_delta if expires_delta is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
        ),
        "iat": int(time.time()),
        "refresh": refresh_token,
        "type": "refresh" if refresh_token else "access",
    }
    
    token = jwt.encode(
        payload=payload, 
        key=settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        token_data = jwt.decode(
            jwt=token, 
            key=settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError as e:
        return None
    except Exception as e:
        return None


def get_user_token(
    user: UserModel,
    is_refresh: bool = False,
) -> str:
    if user.role not in [role.value for role in UserRoles]:
        raise ValueError(f"Invalid user role: {user.role}")
    
    user_data = {
        "id": str(user.user_id),
        "email": user.email,
        "name": user.name,
        "role": user.role,
    }
    
    expiry = timedelta(days=7) if is_refresh else timedelta(hours=1)
    
    return create_access_token(
        user_data=user_data,
        expires_delta=expiry,
        refresh_token=is_refresh,
    )


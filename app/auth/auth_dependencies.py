# app/api/auth/auth_dependencies.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.utils.security import decode_token
from app.models.users.user_model import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_info = token_data.get("user")
    if not user_info:
        raise HTTPException(status_code=401, detail="Token missing user info")

    try:
        user_id = UUID(user_info["id"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")

    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    return user

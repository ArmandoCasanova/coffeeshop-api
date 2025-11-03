# app/api/auth/auth_dependencies.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.utils.security import decode_token
from app.models.users.user_model import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_info = token_data.get("user")
    if not user_info:
        raise HTTPException(status_code=401, detail="Token missing user info")
    # Puedes personalizar la validación aquí si lo necesitas
    user = UserModel(
        user_id=user_info["id"],
        email=user_info["email"],
        name=user_info["name"],
        last_name="",  # El token no incluye last_name, pero es requerido
        role=user_info["role"],
    )
    return user

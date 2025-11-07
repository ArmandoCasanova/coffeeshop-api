# app/api/auth/auth_dependencies.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from app.utils.security import decode_token
from app.models.users.user_model import UserModel
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> UserModel:
    """
    Obtiene el usuario actual desde el token JWT.
    Lee el user_id del token y obtiene el usuario completo de la base de datos.
    """
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_info = token_data.get("user")
    if not user_info:
        raise HTTPException(status_code=401, detail="Token missing user info")
    
    # Obtener el user_id del token
    user_id_str = user_info.get("id")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Token missing user ID")
    
    try:
        user_id = UUID(user_id_str)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=401, detail="Invalid user ID format")
    
    # Obtener el usuario real de la base de datos
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

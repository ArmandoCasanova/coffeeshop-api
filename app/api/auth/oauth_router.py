import logging
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from secrets import token_urlsafe

from app.core.database import get_db
from app.core.redis_client import RedisClient
from app.core.oauth_providers import OAuthProviderFactory
from app.core.session_manager import SessionManager
from app.core.settings import settings
from app.core.sanitizers import InputSanitizer
from app.api.auth.oauth_schema import (
    OAuthStartRequest,
    OAuthCallbackSchema,
    UserOAuthResponseSchema,
)
from app.api.auth.auth_service import AuthService
from app.api.auth.auth_repository import AuthRepository
from app.utils.security import get_user_token


router = APIRouter(prefix="/auth/oauth", tags=["OAuth"])

STATE_KEY_PREFIX = "oauth_state:"
STATE_EXPIRY = 600  # 10 minutes


@router.post("/start")
async def start_oauth_flow(
    provider: str,
    request: Request,
):

    try:
        provider = InputSanitizer.sanitize_string(provider, max_length=50)
        
        if provider not in ["google", "github"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Proveedor no disponible"}
            )
        if provider == "google":
            if not settings.GOOGLE_OAUTH_CLIENT_ID:               
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"error": "Google OAuth no disponible"}
                )
            oauth_provider = OAuthProviderFactory.create_provider(
                "google",
                settings.GOOGLE_OAUTH_CLIENT_ID,
                settings.GOOGLE_OAUTH_CLIENT_SECRET,
                settings.GOOGLE_OAUTH_REDIRECT_URI,
            )
        else:  
            if not settings.GITHUB_OAUTH_CLIENT_ID:                
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"error": "GitHub OAuth no disponible"}
                )
            oauth_provider = OAuthProviderFactory.create_provider(
                "github",
                settings.GITHUB_OAUTH_CLIENT_ID,
                settings.GITHUB_OAUTH_CLIENT_SECRET,
                settings.GITHUB_OAUTH_REDIRECT_URI,
            )
        
        state = token_urlsafe(32)
        redis_client = await RedisClient.get_client()
        await redis_client.setex(f"{STATE_KEY_PREFIX}{state}", STATE_EXPIRY, provider)
        
        auth_url = oauth_provider.get_authorization_url(state)
        
        return {
            "authorization_url": auth_url,
            "provider": provider
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error al iniciar autenticación"}
        )


@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    code: str,
    state: str,
    request: Request,
    session: Session = Depends(get_db),
):

    try:
        provider = InputSanitizer.sanitize_string(provider, max_length=50)        
        redis_client = await RedisClient.get_client()
        stored_provider = await redis_client.get(f"{STATE_KEY_PREFIX}{state}")
        
        if not stored_provider:            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Estado invalido"}
            )
        
        stored_provider = stored_provider.decode() if isinstance(stored_provider, bytes) else stored_provider
        
        if stored_provider != provider:            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Solicitud invalida"}
            )        
        await redis_client.delete(f"{STATE_KEY_PREFIX}{state}")
        
        if provider == "google":
            oauth_provider = OAuthProviderFactory.create_provider(
                "google",
                settings.GOOGLE_OAUTH_CLIENT_ID,
                settings.GOOGLE_OAUTH_CLIENT_SECRET,
                settings.GOOGLE_OAUTH_REDIRECT_URI,
            )
        else:
            oauth_provider = OAuthProviderFactory.create_provider(
                "github",
                settings.GITHUB_OAUTH_CLIENT_ID,
                settings.GITHUB_OAUTH_CLIENT_SECRET,
                settings.GITHUB_OAUTH_REDIRECT_URI,
            )
        
        token_response = await oauth_provider.exchange_code_for_token(code)
        if not token_response:            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Error al procesar la autenticación"}
            )
        
        access_token = token_response.get("access_token")
        if not access_token:            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Solicitud de autenticación invalida"}
            )
        user_info = await oauth_provider.get_user_info(access_token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Solicitud de autenticación invalida"}
            )
                
        user_info["email"] = InputSanitizer.sanitize_email(user_info.get("email", ""))
        user_info["name"] = InputSanitizer.sanitize_string(user_info.get("name", ""))
        
        auth_repository = AuthRepository(session)
        user = await auth_repository.get_user_by_email(user_info["email"])
        
        if not user:
            new_user_data = {
                "email": user_info["email"],
                "name": user_info["name"].split()[0] if user_info["name"] else "User",
                "last_name": " ".join(user_info["name"].split()[1:]) if user_info["name"] and len(user_info["name"].split()) > 1 else "",
                "password": str(uuid4()),
                "role": "customer",
                "is_verified": user_info.get("email_verified", False),
                "oauth_provider": provider,
                "oauth_provider_id": user_info.get("provider_id"),
                "oauth_email_verified": user_info.get("email_verified", False),
                "picture_url": user_info.get("picture"),
                "points": 0.0,
            }
            user = await auth_repository.create_user(new_user_data)            
        else:
            if not user.oauth_provider:
                update_data = {
                    "oauth_provider": provider,
                    "oauth_provider_id": user_info.get("provider_id"),
                    "oauth_email_verified": user_info.get("email_verified", False),
                }
                if user_info.get("picture") and not user.picture_url:
                    update_data["picture_url"] = user_info.get("picture")
                
                await auth_repository.update_user(user.user_id, update_data)
        
        auth_service = AuthService(session)
        tokens = auth_service.generate_tokens_for_user(user)
        
        session_manager = SessionManager(redis_client)
        device_info = {
            "user_agent": request.headers.get("user-agent", ""),
            "ip_address": request.client.host if request.client else "",
        }
        
        session_id = await session_manager.create_session(
            str(user.user_id),
            {
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
            },
            device_info=device_info
        )
        
        return UserOAuthResponseSchema(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            last_name=user.last_name or "",
            role=user.role.value,
            points=user.points,
            oauth_provider=provider,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            session_id=session_id,
            is_verified=user.is_verified,
        )
        
    except HTTPException:
        raise
    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error durante la autenticación"}
        )

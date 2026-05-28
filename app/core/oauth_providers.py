import logging
from typing import Optional, Dict, Any
import httpx
import json



class GoogleOAuthProvider:
    AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTHORIZE_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": self.redirect_uri,
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:    
            return None

    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                response.raise_for_status()
                user_info = response.json()
                
                return {
                    "provider": "google",
                    "provider_id": user_info.get("sub"),
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "picture": user_info.get("picture"),
                    "email_verified": user_info.get("email_verified", False),
                }
        except Exception as e:
            return None


class GitHubOAuthProvider:
    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USERINFO_URL = "https://api.github.com/user"
    EMAIL_URL = "https://api.github.com/user/emails"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user:email",
            "state": state,
            "allow_signup": "true",
        }
        
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTHORIZE_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                token_data = response.json()
                return token_data
        except Exception as e:
            return None

    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.USERINFO_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github.v3+json",
                    },
                )
                response.raise_for_status()
                user_info = response.json()
                
                email_response = await client.get(
                    self.EMAIL_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github.v3+json",
                    },
                )
                email_response.raise_for_status()
                emails = email_response.json()
                
                primary_email = None
                for email_item in emails:
                    if email_item.get("primary"):
                        primary_email = email_item.get("email")
                        break
                
                if not primary_email:
                    for email_item in emails:
                        if email_item.get("verified"):
                            primary_email = email_item.get("email")
                            break
                
                return {
                    "provider": "github",
                    "provider_id": str(user_info.get("id")),
                    "email": primary_email or user_info.get("email"),
                    "name": user_info.get("name") or user_info.get("login"),
                    "picture": user_info.get("avatar_url"),
                    "email_verified": True,
                }
        except Exception as e:
            return None


class OAuthProviderFactory:
    _providers = {
        "google": GoogleOAuthProvider,
        "github": GitHubOAuthProvider,
    }

    @classmethod
    def create_provider(
        cls,
        provider_name: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ):
        if provider_name not in cls._providers:
            raise ValueError(f"Proveedor no soportado: {provider_name}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(client_id, client_secret, redirect_uri)

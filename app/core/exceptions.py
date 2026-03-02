from typing import Optional, Any, Dict
from fastapi import HTTPException, status


class CoffeeShopException(Exception):
    def __init__(self, message: str, code: Optional[str] = None, data: Optional[Any] = None):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)


class AuthenticationError(CoffeeShopException):
    pass


class AuthorizationError(CoffeeShopException):
    pass


class ValidationError(CoffeeShopException):
    pass


class ResourceNotFoundError(CoffeeShopException):
    pass


class ResourceAlreadyExistsError(CoffeeShopException):
    pass


class OAuthError(CoffeeShopException):
    pass


class SessionError(CoffeeShopException):
    pass


class TokenError(CoffeeShopException):
    pass


def exception_to_http_exception(exc: CoffeeShopException, status_code: int = 400) -> HTTPException:
    detail = {
        "error": {
            "message": exc.message,
            "code": exc.code or "UNKNOWN_ERROR",
        }
    }
    if exc.data:
        detail["error"]["data"] = exc.data
    
    return HTTPException(status_code=status_code, detail=detail)

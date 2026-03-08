import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.redis_client import RedisClient
from app.core.settings import settings

LIMIT = getattr(settings, "RATE_LIMIT_REQUESTS", 10)
WINDOW = getattr(settings, "RATE_LIMIT_WINDOW_SECONDS", 60)


def _ip(request: Request) -> str:
    return (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP", "")
        or (request.client.host if request.client else "unknown")
    )


async def _is_over_limit(request: Request) -> bool:
    ip = _ip(request)
    slot = int(time.time() / WINDOW)
    key = f"rl:{ip}:{slot}"
    client = await RedisClient.get_client()
    n = await client.incr(key)
    if n == 1:
        await client.expire(key, WINDOW + 1)
    return n > LIMIT


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if await _is_over_limit(request):
            return JSONResponse(
                status_code=429,
                content={"status": 429, "statusMessage": "Demasiadas solicitudes"},
                headers={"Retry-After": str(WINDOW)},
            )
        return await call_next(request)

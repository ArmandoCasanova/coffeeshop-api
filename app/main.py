from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

# Routers
from app.api.auth.auth_router import router as auth_router
from app.api.auth.oauth_router import router as oauth_router
from app.api.categories.category_router import router as category_router
from app.api.customization.customization_router import router as customization_router
from app.api.dashboard.dashboard_router import router as dashboard_router
from app.api.products.product_router import router as product_router
from app.api.ingredients.ingredient_router import router as ingredient_router
from app.api.orders.order_router import router as orders_router
from app.api.promotions.promotion_router import router as promotion_router
from app.api.promotions_web.promotionweb_router import router as promotion_router_web
from app.api.payments.payments_router import router as payments_router
from app.api.clients.client_router import router as client_router
from app.api.users.user_router import router as user_router
from app.api.reports.report_router import router as report_router

from app.api.notifications.notification_router import router as notifications_router
from app.api.points.points_router import router as points_router


# Configuración
from .core.settings import settings
from .core.redis_client import RedisClient
from .core.exceptions import CoffeeShopException, exception_to_http_exception

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisClient.get_client()
    logger.info("Redis connection established")
    yield

    await RedisClient.close()
    logger.info("Redis connection closed")


# Crear instancia de FastAPI con la configuración del proyecto
app = FastAPI(
    title=(
        settings.PROJECT_NAME if hasattr(settings, "PROJECT_NAME") else "CoffeeShop API"
    ),
    description="API para gestión de cafetería con autenticación segura (JWT, OAuth2, Sesiones)",
    version="2.0.0",
    openapi_url=f"{settings.API_V1}/openapi.json",
    lifespan=lifespan,
)

# Middleware de seguridad y rendimiento
# 1. Hosts de confianza
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # En producción, especificar dominios permitidos
)

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, usar lista específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# 3. Compresión GZIP
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Manejo central de excepciones
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    """Manejo de excepciones HTTP de FastAPI"""
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "statusMessage": exc.detail,
        }
    )


@app.exception_handler(CoffeeShopException)
async def coffeeshop_exception_handler(_, exc: CoffeeShopException):
    """Manejo de excepciones personalizadas de la aplicación"""
    status_code = 400
    
    # Mapear tipo de excepción a código HTTP
    exception_type = type(exc).__name__
    if exception_type == "AuthenticationError":
        status_code = 401
    elif exception_type == "AuthorizationError":
        status_code = 403
    elif exception_type == "ResourceNotFoundError":
        status_code = 404
    elif exception_type == "ResourceAlreadyExistsError":
        status_code = 409
    
    http_exc = exception_to_http_exception(exc, status_code)
    return JSONResponse(status_code=http_exc.status_code, content=http_exc.detail)


# Registrar routers
app.include_router(auth_router, prefix=settings.API_V1, tags=["Auth"])
app.include_router(oauth_router, prefix=settings.API_V1, tags=["OAuth"])
app.include_router(product_router, prefix=settings.API_V1, tags=["Products"])
app.include_router(ingredient_router, prefix=settings.API_V1, tags=["Ingredients"])
app.include_router(customization_router, prefix=settings.API_V1, tags=["Customization"])
app.include_router(dashboard_router, prefix=settings.API_V1, tags=["Dashboard"])
app.include_router(orders_router, prefix=settings.API_V1, tags=["Orders"])
app.include_router(category_router, prefix=settings.API_V1, tags=["Categories"])
app.include_router(promotion_router, prefix=settings.API_V1, tags=["Promotions"])
app.include_router(promotion_router_web, prefix=settings.API_V1, tags=["PromotionsWeb"])
app.include_router(payments_router, prefix=settings.API_V1, tags=["Payments"])
app.include_router(client_router, prefix=settings.API_V1, tags=["Clients"])
app.include_router(user_router, prefix=settings.API_V1, tags=["Users"])
app.include_router(report_router, prefix=settings.API_V1, tags=["Reports"])
app.include_router(notifications_router, prefix=settings.API_V1, tags=["Notifications"])
app.include_router(points_router, prefix=settings.API_V1, tags=["Points"])


@app.get("/")
def read_root():
    return {
        "message": "Welcome to CoffeeShop API ☕",
        "version": "2.0.0",
        "endpoints": {
            "docs": f"{settings.API_V1}/docs",
            "redoc": f"{settings.API_V1}/redoc",
        }
    }


@app.get("/health")
def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "service": "CoffeeShop API",
    }
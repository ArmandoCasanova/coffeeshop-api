from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Routers
from app.api.auth.auth_router import router as auth_router
from app.api.categories.category_router import category_router
from app.api.dashboard.dashboard_router import router as dashboard_router
from app.api.products.product_router import router as product_router
from app.api.ingredients.ingredient_router import router as ingredient_router
from app.api.orders.order_router import router as orders_router
from app.api.promotions.promotion_router import router as promotion_router
from app.api.payments.payments_router import router as payments_router
from app.api.clients.client_router import router as client_router
from app.api.users.user_router import router as user_router


# Configuración
from .core.settings import settings
from .core.redis_client import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar Redis
    await RedisClient.get_client()
    print("✅ Redis connection established")
    yield
    # Shutdown: Cerrar conexión Redis
    await RedisClient.close()
    print("❌ Redis connection closed")


# Crear instancia de FastAPI con la configuración del proyecto
app = FastAPI(
    title=(
        settings.PROJECT_NAME if hasattr(settings, "PROJECT_NAME") else "CoffeeShop API"
    ),
    description="API para gestión de cafetería",
    version="1.0.0",
    openapi_url=f"{settings.API_V1}/openapi.json",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
]

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejo global de excepciones HTTP
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


# Incluir routers con prefijos y tags
app.include_router(auth_router, prefix=settings.API_V1, tags=["Auth"])
app.include_router(product_router, prefix=settings.API_V1, tags=["Products"])
app.include_router(ingredient_router, prefix=settings.API_V1, tags=["Ingredients"])
app.include_router(dashboard_router, prefix=settings.API_V1, tags=["Dashboard"])
app.include_router(orders_router, prefix=settings.API_V1, tags=["Orders"])
app.include_router(category_router, prefix=settings.API_V1, tags=["Categories"])
app.include_router(promotion_router, prefix=settings.API_V1, tags=["Promotions"])
app.include_router(payments_router, prefix=settings.API_V1, tags=["Payments"])
app.include_router(client_router, prefix=settings.API_V1, tags=["Clients"])
app.include_router(user_router, prefix=settings.API_V1, tags=["Users"])


# Endpoint raíz de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to CoffeeShop API ☕"}

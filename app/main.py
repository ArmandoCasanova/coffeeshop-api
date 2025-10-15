
from fastapi import FastAPI
from app.api.auth.auth_router import router as auth_router
from app.api.products.product_router import router as product_router
from app.api.ingredients.ingredient_router import router as ingredient_router
from app.core.settings import settings

app = FastAPI(
    title="CoffeeShop API",
    description="API para gestión de cafetería",
    version="1.0.0"
)

# Incluir routers
app.include_router(auth_router, prefix=settings.API_V1)
app.include_router(product_router, prefix=settings.API_V1)
app.include_router(ingredient_router, prefix=settings.API_V1)

@app.get("/")
def read_root():
    return {"Hello": "World"}
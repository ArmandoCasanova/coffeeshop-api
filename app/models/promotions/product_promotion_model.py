from sqlmodel import SQLModel, Field
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID

class ProductPromotionModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "product_promotions"
    product_id: UUID = Field(foreign_key="products.product_id", primary_key=True)
    promotion_id: UUID = Field(foreign_key="promotions.promotion_id", primary_key=True)

from sqlmodel import SQLModel, Field

class ProductPromotionModel(SQLModel, table=True):
    __tablename__ = "product_promotions"
    product_id: int = Field(foreign_key="products.product_id", primary_key=True)
    promotion_id: int = Field(foreign_key="promotions.promotion_id", primary_key=True)

from sqlmodel import Field, SQLModel
from uuid import UUID

class UserFavoriteModel(SQLModel, table=True):
    __tablename__ = "user_favorites"
    user_id: UUID = Field(foreign_key="users.user_id", primary_key=True)
    product_id: UUID = Field(foreign_key="products.product_id", primary_key=True)

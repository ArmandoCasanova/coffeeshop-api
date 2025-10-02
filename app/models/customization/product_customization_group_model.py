from sqlmodel import SQLModel, Field
from uuid import UUID

class ProductCustomizationGroupModel(SQLModel, table=True):
    __tablename__ = "product_customization_groups"
    product_id: UUID = Field(foreign_key="products.product_id", primary_key=True)
    group_id: UUID = Field(foreign_key="customization_groups.group_id", primary_key=True)

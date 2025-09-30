from sqlmodel import SQLModel, Field

class OrderItemCustomizationModel(SQLModel, table=True):
    __tablename__ = "order_item_customization"
    order_item_id: int = Field(foreign_key="order_item.order_item_id", primary_key=True)
    option_id: int = Field(foreign_key="customization_options.option_id", primary_key=True)
    extra_cost_at_purchase: float

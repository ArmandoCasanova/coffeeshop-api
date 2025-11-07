from sqlmodel import Field
from app.core.base_model import BaseCoffeeAppModel
from uuid import UUID, uuid4


class StripeCustomerModel(BaseCoffeeAppModel, table=True):
    __tablename__ = "stripe_customers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id", nullable=False)
    customer_id: str = Field(unique=True, nullable=False, max_length=50)
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

# Este archivo solo contendrá el modelo de métodos de pago
class UserPaymentMethodModel(SQLModel, table=True):
    __tablename__ = "user_payment_methods"
    payment_method_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    provider_token: str
    card_last_four: str
    is_default: bool = Field(default=False)

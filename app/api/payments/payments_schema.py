from pydantic import BaseModel
from uuid import UUID

class PaymentRequest(BaseModel):
    amount: int
    currency: str = "mxn"

class PayWithSavedMethodRequest(BaseModel):
    amount: int
    currency: str
    user_id: UUID
    payment_method_id: str


class AttachPaymentMethodRequest(BaseModel):
    payment_method_id: str
    customer_id: str


import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/payment", tags=["Payments"])

class PaymentRequest(BaseModel):
    amount: int
    currency: str = "usd"

@router.post("/create-payment-intent")
async def create_payment_intent(payment_data: PaymentRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment_data.amount,
            currency=payment_data.currency,
            automatic_payment_methods={"enabled": True},
        )
        
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
        
    except Exception as e:  
        raise HTTPException(status_code=400, detail=str(e))
   
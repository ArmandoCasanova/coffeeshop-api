import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/payment", tags=["Payments"])

class PaymentRequest(BaseModel):
    amount: int
    currency: str = "usd"

class PayWithSavedMethodRequest(BaseModel):
    amount: int
    currency: str
    customer_id: str
    payment_method_id: str

class AttachPaymentMethodRequest(BaseModel):
    payment_method_id: str
    customer_id: str


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
    

@router.post("/create-customer/{user_id}")
async def create_customer(user_id: str):
    try:
        customer = stripe.Customer.create()
        # Aquí se debe guardar el customer.id asociado al user_id
        print(customer.id)
        return {"customer_id": customer.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-setup-intent/{customer_id}")
async def create_setup_intent(customer_id: str):
    try:
        setup_intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=["card"]
        )
        return {"client_secret": setup_intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🆕 NUEVA RUTA: Adjuntar PaymentMethod al Cliente y Confirmar SetupIntent
@router.post("/attach-payment-method")
async def attach_payment_method(data: AttachPaymentMethodRequest):
    try:
        # 1. Adjuntar PaymentMethod al cliente
        payment_method = stripe.PaymentMethod.attach(
            data.payment_method_id,
            customer=data.customer_id
        )
        
        # 2. Confirmar SetupIntent automáticamente
        # (Asumiendo que ya existe uno pendiente para este cliente)
        setup_intents = stripe.SetupIntent.list(
            customer=data.customer_id,
            limit=1
        )
        
        if setup_intents.data:
            setup_intent = stripe.SetupIntent.confirm(
                setup_intents.data[0].id,
                payment_method=data.payment_method_id
            )
            return {
                "success": True,
                "payment_method_id": payment_method.id,
                "setup_intent_status": setup_intent.status
            }
        
        return {"success": True, "payment_method_id": payment_method.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list-payment-methods/{customer_id}")
async def list_payment_methods(customer_id: str):
    try:
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )
        return {"data": payment_methods.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pay-with-saved-method")
async def pay_with_saved_method(data: PayWithSavedMethodRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=data.amount,
            currency=data.currency,
            customer=data.customer_id,
            payment_method=data.payment_method_id,
            confirm=True,
            off_session=True,
        )

        return {"status": intent.status, "id": intent.id}

    except stripe.error.CardError as e:
        raise HTTPException(status_code=400, detail=f"Error de tarjeta: {e.user_message}")
    except stripe.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=f"Solicitud inválida: {e.user_message}")
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Error en Stripe: {e.user_message}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error general: {str(e)}")


@router.delete("/delete-payment-method/{payment_method_id}")
async def delete_payment_method(payment_method_id: str):
    """
    Desvincula un método de pago de un cliente en Stripe.
    """
    try:
        detached = stripe.PaymentMethod.detach(payment_method_id)
        return {"message": "Método de pago eliminado correctamente", "id": detached.id}
    except stripe.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=f"Error en la solicitud: {e.user_message}")
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Error en Stripe: {e.user_message}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error general: {str(e)}")
# app/api/routes/payment_router.py
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from app.api.payments.payments_controller import PaymentController
from app.api.payments.payments_schema import PaymentRequest, PayWithSavedMethodRequest,AttachPaymentMethodRequest
from sqlmodel import Session
from app.core.database import get_db
from uuid import UUID
router = APIRouter(prefix="/payment", tags=["Payments"])


@router.post("/create-payment-intent")
async def create_payment_intent(payment_data: PaymentRequest):
    return PaymentController.create_payment_intent(payment_data.amount, payment_data.currency)


@router.post("/create-customer/{user_id}")
async def create_customer(user_id: str):
    return PaymentController.create_customer(user_id)


@router.post("/create-setup-intent/{user_id}")
async def create_setup_intent(user_id: UUID, session: Session = Depends(get_db)):
    controller = PaymentController(session)
    return await controller.create_setup_intent(user_id)


@router.post("/attach-payment-method")
async def attach_payment_method(data: AttachPaymentMethodRequest):
    return PaymentController.attach_payment_method(data.payment_method_id, data.customer_id)


@router.get("/list-payment-methods/{user_id}")
async def list_payment_methods(user_id: UUID, session: Session = Depends(get_db)):
    controller = PaymentController(session)
    return await controller.list_payment_methods(user_id)


@router.post("/pay-with-saved-method")
async def pay_with_saved_method(data: PayWithSavedMethodRequest, session: Session = Depends(get_db)):
    controller = PaymentController(session)
    return await controller.pay_with_saved_method(
        data.amount, data.currency, data.user_id, data.payment_method_id
    )

@router.delete("/delete-payment-method/{payment_method_id}")
async def delete_payment_method(payment_method_id: str):
    return PaymentController.delete_payment_method(payment_method_id)


# Ensure a Stripe customer exists for the given user
@router.get("/customer/{user_id}")
async def get_or_create_customer(user_id: str, session: Session = Depends(get_db)):
    controller = PaymentController(session)
    return controller.ensure_customer(user_id)


# Create an ephemeral key for CustomerSheet/PaymentSheet
@router.post("/ephemeral-key/{user_id}")
async def create_ephemeral_key(
    user_id: str,
    session: Session = Depends(get_db),
    stripe_version: str | None = Header(default=None, alias="Stripe-Version"),
):
    controller = PaymentController(session)
    return controller.create_ephemeral_key(user_id, stripe_version)


# Lightweight mobile error logging to help debug release crashes
class MobileLog(BaseModel):
    message: str
    stack: str | None = None
    context: dict | None = None


@router.post("/mobile-error-log")
async def mobile_error_log(payload: MobileLog):
    print("[MOBILE_ERROR]", payload.message)
    if payload.stack:
        print(payload.stack)
    if payload.context:
        print(payload.context)
    return {"ok": True}

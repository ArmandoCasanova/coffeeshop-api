# app/services/payment_service.py
import stripe
from app.core.settings import settings
from app.models.payments.stripe_customers_model import StripeCustomerModel
from uuid import UUID
from app.core.http_response import CoffeeAppHttpResponse
from sqlmodel import select
from fastapi import HTTPException


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def create_payment_intent(amount: int, currency: str):
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )

    @staticmethod
    def create_customer():
        return stripe.Customer.create()

    @staticmethod
    def create_setup_intent(customer_id: str):
        return stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=["card"]
        )

    @staticmethod
    def attach_payment_method(payment_method_id: str, customer_id: str):
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id
        )

        setup_intents = stripe.SetupIntent.list(customer=customer_id, limit=1)

        if setup_intents.data:
            setup_intent = stripe.SetupIntent.confirm(
                setup_intents.data[0].id,
                payment_method=payment_method_id
            )
            return {
                "payment_method_id": payment_method.id,
                "setup_intent_status": setup_intent.status
            }

        return {"payment_method_id": payment_method.id}

    @staticmethod
    def list_payment_methods(customer_id: str):
        return stripe.PaymentMethod.list(customer=customer_id, type="card")

    @staticmethod
    def pay_with_saved_method(amount: int, currency: str, customer_id: str, payment_method_id: str):
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            customer=customer_id,
            payment_method=payment_method_id,
            confirm=True,
            off_session=True,
        )

    @staticmethod
    def delete_payment_method(payment_method_id: str):
        return stripe.PaymentMethod.detach(payment_method_id)
        

    def create_stripe_customer(self, user_id: str):
        stripe_customer = stripe.Customer.create()

        new_customer = StripeCustomerModel(
            user_id=user_id,
            customer_id=stripe_customer["id"]
        )

        self.session.add(new_customer)
        self.session.commit()
        self.session.refresh(new_customer)

        return new_customer

    async def get_customer_id_with_user_id(self, user_id: UUID):
        try:
            statement = select(StripeCustomerModel).where(StripeCustomerModel.user_id == user_id)
            result = self.session.exec(statement)
            customer = result.first()

            if not customer:
                raise HTTPException(status_code=404, detail="customer_id no encontrado")

            return customer.customer_id

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener customer_id: {e}")


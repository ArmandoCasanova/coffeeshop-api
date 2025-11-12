# app/controllers/payment_controller.py
from fastapi import HTTPException
from app.api.payments.payments_service import PaymentService
from sqlmodel import Session
from uuid import UUID


class PaymentController:
    def __init__(self, session: Session):
        self.payment_service = PaymentService(session)

    @staticmethod
    def create_payment_intent(amount: int, currency: str):
        try:
            intent = PaymentService.create_payment_intent(amount, currency)
            return {"client_secret": intent.client_secret, "payment_intent_id": intent.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def create_customer(user_id: str):
        try:
            customer = PaymentService.create_customer()
            return {"customer_id": customer.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    async def create_setup_intent(self, user_id: UUID):
        try:
            try:
                customer_id = await self.payment_service.get_customer_id_with_user_id(user_id)
            except HTTPException as he:
                if he.status_code == 404:
                    customer_id = self.payment_service.ensure_customer_for_user(str(user_id))
                else:
                    raise
            setup_intent = PaymentService.create_setup_intent(customer_id)
            return {"client_secret": setup_intent.client_secret}
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error al crear setup intent: {e}")
            raise HTTPException(status_code=500, detail=f"Error al crear configuración de pago: {str(e)}")

    @staticmethod
    def attach_payment_method(payment_method_id: str, customer_id: str):
        try:
            result = PaymentService.attach_payment_method(payment_method_id, customer_id)
            return {"success": True, **result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def list_payment_methods(self, user_id: UUID):
        try:
            try:
                customer_id = await self.payment_service.get_customer_id_with_user_id(user_id)
            except HTTPException as he:
                if he.status_code == 404:
                    return {"data": []}
                else:
                    raise
            result = PaymentService.list_payment_methods(customer_id)
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    async def pay_with_saved_method(self, amount: int, currency: str, user_id: UUID, payment_method_id: str):
        try:
            customer_id = await self.payment_service.get_customer_id_with_user_id(user_id)
            intent = PaymentService.pay_with_saved_method(amount, currency, customer_id, payment_method_id)
            return {"status": intent.status, "id": intent.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_payment_method(payment_method_id: str):
        try:
            result = PaymentService.delete_payment_method(payment_method_id)
            return {"message": "Método de pago eliminado correctamente", "id": result.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        
    def create_stripe_customer(self, user_id: str):
        try:
            return self.payment_service.create_stripe_customer(user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def ensure_customer(self, user_id: str):
        try:
            return {"customer_id": self.payment_service.ensure_customer_for_user(user_id)}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def create_ephemeral_key(self, user_id: str, api_version: str | None = None):
        try:
            customer_id = self.payment_service.ensure_customer_for_user(user_id)
            ek = PaymentService.create_ephemeral_key(customer_id, api_version)
            return ek
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
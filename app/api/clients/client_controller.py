from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
import logging

# --- CAMBIOS ---
from app.api.clients.client_service import ClientService
from app.api.clients.client_schema import (
    ClientCreateSchema,
    ClientUpdateSchema,
    ClientResponseSchema,
    ClientListResponseSchema,
)

logger = logging.getLogger(__name__)

class ClientController:
    def __init__(self, session: Session):
        self.session = session
        self.service = ClientService(session)  

    async def create_client(
        self, client_data: ClientCreateSchema
    ) -> ClientResponseSchema:
        try:
            client = await self.service.create_client(client_data)
            return ClientResponseSchema.model_validate(client)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_client(self, user_id: UUID) -> ClientResponseSchema:
        try:
            client = await self.service.get_client_by_id(user_id)
            if not client:
                CoffeeAppHttpResponse.not_found(message="Client not found")

            return ClientResponseSchema.model_validate(client)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_all_clients(
        self, page: int = 1, page_size: int = 10, is_verified: Optional[bool] = None
    ) -> ClientListResponseSchema:
        try:
            skip = (page - 1) * page_size
            clients, total = await self.service.get_all_clients(
                skip, page_size, is_verified
            )

            client_list = [
                ClientResponseSchema.model_validate(client) for client in clients
            ]

            return ClientListResponseSchema(
                clients=client_list, total=total, page=page, page_size=page_size
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_client(
        self, user_id: UUID, client_data: ClientUpdateSchema
    ) -> ClientResponseSchema:
        try:
            client = await self.service.update_client(user_id, client_data)
            if not client:
                CoffeeAppHttpResponse.not_found(message="Client not found")

            return ClientResponseSchema.model_validate(client)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def delete_client(self, user_id: UUID) -> dict:
        try:
            deleted = await self.service.delete_client(user_id)
            if not deleted:
                CoffeeAppHttpResponse.not_found(message="Client not found")

            return {"message": "Client deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
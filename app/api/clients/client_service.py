from app.core.http_response import CoffeeAppHttpResponse
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException
from uuid import UUID
from passlib.context import CryptContext  

from app.api.clients.client_schema import (
    ClientCreateSchema,
    ClientUpdateSchema,
    UserRole,
)
from app.api.clients.client_repository import ClientRepository
from app.models.users.user_model import UserModel 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ClientService:
    def __init__(self, session: Session):
        self.client_repository = ClientRepository(session)

    async def create_client(self, client_data: ClientCreateSchema) -> UserModel:
        try:
            existing = await self.client_repository.get_user_by_email(client_data.email)
            if existing:
                CoffeeAppHttpResponse.conflict(message="Email already registered")

            client_dict = client_data.model_dump()
            
            hashed_password = pwd_context.hash(client_dict.pop("password"))
            client_dict["password"] = hashed_password
            
            client_dict["role"] = UserRole.customer

            return await self.client_repository.create_client(client_dict)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_client_by_id(self, user_id: UUID) -> Optional[UserModel]:
        try:
            return await self.client_repository.get_client_by_id(user_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def get_all_clients(
        self, skip: int = 0, limit: int = 10, is_verified: Optional[bool] = None
    ) -> tuple[list, int]:
        try:
            return await self.client_repository.get_all_clients(
                skip, limit, is_verified
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def update_client(
        self, user_id: UUID, client_data: ClientUpdateSchema
    ) -> Optional[UserModel]:
        try:
            update_data = client_data.model_dump(exclude_unset=True)

            if "email" in update_data:
                existing = await self.client_repository.get_user_by_email(update_data["email"])
                if existing and existing.user_id != user_id:
                    CoffeeAppHttpResponse.conflict(message="Email already registered by another user")
            
            update_data.pop("password", None)

            return await self.client_repository.update_client(
                user_id, update_data
            )
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()

    async def delete_client(self, user_id: UUID) -> bool:
        try:
            return await self.client_repository.delete_client(user_id)
        except HTTPException:
            raise
        except Exception as e:
            CoffeeAppHttpResponse.internal_error()
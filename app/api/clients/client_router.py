from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.api.clients.client_controller import ClientController
from app.api.clients.client_schema import (
    ClientCreateSchema,
    ClientUpdateSchema,
    ClientResponseSchema,
    ClientListResponseSchema,
)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponseSchema, status_code=201)
async def create_client(
    client_data: ClientCreateSchema, session: Session = Depends(get_db)
):
    controller = ClientController(session)
    return await controller.create_client(client_data)


@router.get("/", response_model=ClientListResponseSchema)
async def get_all_clients(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    session: Session = Depends(get_db),
):
    controller = ClientController(session)
    return await controller.get_all_clients(page, page_size, is_verified)


@router.get("/{user_id}", response_model=ClientResponseSchema)
async def get_client(user_id: UUID, session: Session = Depends(get_db)):
    controller = ClientController(session)
    return await controller.get_client(user_id)


@router.put("/{user_id}", response_model=ClientResponseSchema)
async def update_client(
    user_id: UUID,
    client_data: ClientUpdateSchema,
    session: Session = Depends(get_db),
):
    controller = ClientController(session)
    return await controller.update_client(user_id, client_data)


@router.delete("/{user_id}")
async def delete_client(user_id: UUID, session: Session = Depends(get_db)):
    controller = ClientController(session)
    return await controller.delete_client(user_id)
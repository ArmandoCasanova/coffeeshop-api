from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from uuid import UUID
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"

class ClientCreateSchema(BaseModel):
    name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8, description="La contraseña será hasheada")
    birth_date: Optional[date] = None

class ClientUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    points: Optional[float] = Field(None, ge=0)
    is_verified: Optional[bool] = None

class OrderSummarySchema(BaseModel):
    """Define la estructura de cada orden en la lista de resumen del cliente."""
    order_id: UUID
    total_amount: float
    order_date: datetime

    class Config:
        from_attributes = True

class ClientResponseSchema(BaseModel):
    # Campos de UserModel
    user_id: UUID
    role: UserRole
    name: str
    last_name: str
    birth_date: Optional[date]
    email: EmailStr
    points: float
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    total_orders: int = Field(default=0)
    total_spent: float = Field(default=0.0)
    last_order_date: Optional[datetime] = Field(None)
    
    completed_orders: List[OrderSummarySchema] = Field(
        default_factory=list, 
        description="Lista de órdenes completadas (ID, monto y fecha)"
    )

    class Config:
        from_attributes = True
        
class ClientListResponseSchema(BaseModel):
    clients: List[ClientResponseSchema]
    total: int
    page: int = 1
    page_size: int = 10
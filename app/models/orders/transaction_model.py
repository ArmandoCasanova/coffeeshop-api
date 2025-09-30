from typing import Optional
from sqlmodel import SQLModel, Field, Column, Enum
from datetime import datetime
import enum

class TransactionStatus(str, enum.Enum):
    success = "success"
    failed = "failed"

class TransactionModel(SQLModel, table=True):
    __tablename__ = "transactions"
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    amount: float
    status: TransactionStatus = Field(sa_column=Column(Enum(TransactionStatus), nullable=False))
    transaction_date: datetime = Field(default_factory=datetime.utcnow)

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    user_id: int
    amount: float
    category: str
    description: Optional[str] = None
    transaction_date: date
    transaction_type: str = "expense"


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    transaction_date: Optional[date] = None
    transaction_type: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
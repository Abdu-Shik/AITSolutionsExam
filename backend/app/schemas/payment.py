from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus, PaymentMethod


class PaymentCreate(BaseModel):
    booking_id: int
    transaction_id: str  # For idempotency


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: str
    created_at: datetime

    class Config:
        from_attributes = True


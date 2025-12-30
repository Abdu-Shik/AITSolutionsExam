from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    flight_id: int
    passenger_profiles: List[dict]  # List of {passenger_profile_id, seat_number}


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: int
    pnr: str
    user_id: int
    flight_id: int
    status: BookingStatus
    seat_hold_expires_at: Optional[datetime]
    created_at: datetime
    flight: dict
    tickets: List[dict]

    class Config:
        from_attributes = True


class BookingDetailResponse(BookingResponse):
    payment: Optional[dict] = None


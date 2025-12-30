from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.flight import FlightStatus


class FlightBase(BaseModel):
    flight_number: str
    origin_id: int
    destination_id: int
    airplane_id: int
    scheduled_departure: datetime
    scheduled_arrival: datetime
    gate: Optional[str] = None
    terminal: Optional[str] = None
    status: Optional[FlightStatus] = FlightStatus.SCHEDULED


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    origin_id: Optional[int] = None
    destination_id: Optional[int] = None
    airplane_id: Optional[int] = None
    scheduled_departure: Optional[datetime] = None
    scheduled_arrival: Optional[datetime] = None
    gate: Optional[str] = None
    terminal: Optional[str] = None
    status: Optional[FlightStatus] = None


class FlightSearch(BaseModel):
    origin: Optional[str] = None  # Airport code
    destination: Optional[str] = None  # Airport code
    date: Optional[datetime] = None


class FlightResponse(FlightBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FlightDetailResponse(FlightResponse):
    origin_airport: dict
    destination_airport: dict
    airplane: dict
    available_seats: int
    total_seats: int


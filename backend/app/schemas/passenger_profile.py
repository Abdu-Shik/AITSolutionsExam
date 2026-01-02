from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class PassengerProfileBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    passport_number: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[date] = None


class PassengerProfileCreate(PassengerProfileBase):
    pass


class PassengerProfileUpdate(PassengerProfileBase):
    pass


class PassengerProfileResponse(PassengerProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


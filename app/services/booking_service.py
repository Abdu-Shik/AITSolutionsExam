from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import string
import random
from app.models.booking import Booking, BookingStatus
from app.models.ticket import Ticket
from app.models.payment import Payment, PaymentStatus
from app.models.flight import Flight
from app.models.passenger_profile import PassengerProfile


def generate_pnr() -> str:
    """Generate a unique 6-character PNR"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def generate_ticket_number() -> str:
    """Generate a unique ticket number"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def create_booking(
    db: Session,
    user_id: int,
    flight_id: int,
    passenger_profiles: list
) -> Booking:
    # Check if flight exists
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    # Check if user has passenger profile
    passenger_profile = db.query(PassengerProfile).filter(
        PassengerProfile.user_id == user_id
    ).first()
    if not passenger_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your passenger profile before booking"
        )
    
    # Check seat availability and prevent double booking
    # Also clean up expired seat holds
    now = datetime.utcnow()
    expired_bookings = db.query(Booking).filter(
        Booking.flight_id == flight_id,
        Booking.status == BookingStatus.CREATED,
        Booking.seat_hold_expires_at < now
    ).all()
    for expired_booking in expired_bookings:
        expired_booking.status = BookingStatus.CANCELLED
    
    booked_seats = set()
    for ticket in db.query(Ticket).join(Booking).filter(
        Booking.flight_id == flight_id,
        Booking.status != BookingStatus.CANCELLED
    ).all():
        booked_seats.add(ticket.seat_number)
    
    # Validate seats and passenger profiles
    for passenger_data in passenger_profiles:
        seat = passenger_data.get("seat_number")
        passenger_profile_id = passenger_data.get("passenger_profile_id")
        
        # Validate seat
        if seat in booked_seats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {seat} is already booked"
            )
        booked_seats.add(seat)
        
        # Validate passenger profile exists and belongs to user
        passenger_profile = db.query(PassengerProfile).filter(
            PassengerProfile.id == passenger_profile_id,
            PassengerProfile.user_id == user_id
        ).first()
        if not passenger_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Passenger profile {passenger_profile_id} not found or does not belong to user"
            )
    
    # Create booking with 10-minute hold
    pnr = generate_pnr()
    while db.query(Booking).filter(Booking.pnr == pnr).first():
        pnr = generate_pnr()
    
    booking = Booking(
        pnr=pnr,
        user_id=user_id,
        flight_id=flight_id,
        status=BookingStatus.CREATED,
        seat_hold_expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(booking)
    db.flush()
    
    # Create tickets
    for passenger_data in passenger_profiles:
        ticket = Ticket(
            ticket_number=generate_ticket_number(),
            booking_id=booking.id,
            passenger_profile_id=passenger_data["passenger_profile_id"],
            seat_number=passenger_data["seat_number"]
        )
        db.add(ticket)
    
    db.commit()
    db.refresh(booking)
    return booking


def get_user_bookings(db: Session, user_id: int, upcoming_only: bool = False):
    query = db.query(Booking).filter(Booking.user_id == user_id)
    
    if upcoming_only:
        query = query.join(Flight).filter(
            Flight.scheduled_departure > datetime.utcnow()
        )
    else:
        query = query.join(Flight).filter(
            Flight.scheduled_departure < datetime.utcnow()
        )
    
    return query.all()


def cancel_booking(db: Session, booking_id: int, user_id: int = None):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if user_id and booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking"
        )
    
    booking.status = BookingStatus.CANCELLED
    db.commit()
    return booking


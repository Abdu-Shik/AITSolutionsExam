from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import json
from app.models.checkin import CheckIn
from app.models.ticket import Ticket
from app.models.booking import Booking
from app.models.flight import Flight
from app.models.passenger_profile import PassengerProfile


def check_in(
    db: Session,
    ticket_id: int,
    user_id: int
) -> CheckIn:
    # Get ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Verify ticket belongs to user
    booking = db.query(Booking).filter(Booking.id == ticket.booking_id).first()
    if booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check in for this ticket"
        )
    
    # Get flight
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    # Check timing (24h to 1h before departure)
    now = datetime.utcnow()
    time_until_departure = flight.scheduled_departure - now
    
    if time_until_departure > timedelta(hours=24):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-in opens 24 hours before departure"
        )
    
    if time_until_departure < timedelta(hours=1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-in closes 1 hour before departure"
        )
    
    # Check if already checked in
    existing_checkin = db.query(CheckIn).filter(CheckIn.ticket_id == ticket_id).first()
    if existing_checkin:
        return existing_checkin
    
    # Get passenger profile
    passenger = db.query(PassengerProfile).filter(
        PassengerProfile.id == ticket.passenger_profile_id
    ).first()
    
    # Generate QR code payload (JSON with ticket and flight info)
    qr_payload = {
        "ticket_number": ticket.ticket_number,
        "pnr": booking.pnr,
        "flight_number": flight.flight_number,
        "passenger_name": passenger.full_name,
        "seat": ticket.seat_number,
        "gate": flight.gate,
        "terminal": flight.terminal,
        "departure": flight.scheduled_departure.isoformat()
    }
    qr_code = json.dumps(qr_payload)
    
    # Create check-in
    checkin = CheckIn(
        ticket_id=ticket_id,
        qr_code=qr_code
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


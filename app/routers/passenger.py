from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_passenger
from app.models.user import User
from app.schemas.flight import FlightSearch, FlightResponse, FlightDetailResponse
from app.schemas.booking import BookingCreate, BookingResponse, BookingDetailResponse
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.schemas.checkin import CheckInResponse
from app.schemas.announcement import AnnouncementResponse
from app.services.flight_service import search_flights, get_flight_details, get_seat_map
from app.services.booking_service import create_booking, get_user_bookings, cancel_booking
from app.services.payment_service import process_payment
from app.services.checkin_service import check_in
from app.models.announcement import Announcement
from app.models.ticket import Ticket
from app.models.payment import Payment

router = APIRouter(prefix="/passenger", tags=["Passenger"])


@router.get("/flights/search", response_model=List[FlightResponse])
def search_flights_endpoint(
    origin: str = None,
    destination: str = None,
    date: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Search flights by origin, destination, and date"""
    from datetime import datetime
    
    parsed_date = None
    if date:
        try:
            # Try ISO format first
            parsed_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except ValueError:
            try:
                # Try common date formats
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS) or YYYY-MM-DD"
                )
    
    search_params = FlightSearch(
        origin=origin,
        destination=destination,
        date=parsed_date
    )
    flights = search_flights(db, search_params)
    return flights


@router.get("/flights/{flight_id}", response_model=FlightDetailResponse)
def get_flight_details_endpoint(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Get flight details with available seats"""
    result = get_flight_details(db, flight_id)
    flight = result["flight"]
    
    return {
        "id": flight.id,
        "flight_number": flight.flight_number,
        "origin_id": flight.origin_id,
        "destination_id": flight.destination_id,
        "airplane_id": flight.airplane_id,
        "scheduled_departure": flight.scheduled_departure,
        "scheduled_arrival": flight.scheduled_arrival,
        "gate": flight.gate,
        "terminal": flight.terminal,
        "status": flight.status,
        "created_at": flight.created_at,
        "origin_airport": {
            "id": flight.origin_airport.id,
            "code": flight.origin_airport.code,
            "name": flight.origin_airport.name,
            "city": flight.origin_airport.city,
            "country": flight.origin_airport.country
        },
        "destination_airport": {
            "id": flight.destination_airport.id,
            "code": flight.destination_airport.code,
            "name": flight.destination_airport.name,
            "city": flight.destination_airport.city,
            "country": flight.destination_airport.country
        },
        "airplane": {
            "id": flight.airplane.id,
            "model": flight.airplane.model,
            "registration_number": flight.airplane.registration_number,
            "total_seats": flight.airplane.total_seats
        },
        "available_seats": result["available_seats"],
        "total_seats": result["total_seats"]
    }


@router.get("/flights/{flight_id}/seat-map")
def get_seat_map_endpoint(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Get seat map for a flight"""
    return get_seat_map(db, flight_id)


@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking_endpoint(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Create a new booking"""
    booking = create_booking(
        db,
        current_user.id,
        booking_data.flight_id,
        booking_data.passenger_profiles
    )
    
    # Format response
    tickets = db.query(Ticket).filter(Ticket.booking_id == booking.id).all()
    return {
        "id": booking.id,
        "pnr": booking.pnr,
        "user_id": booking.user_id,
        "flight_id": booking.flight_id,
        "status": booking.status,
        "seat_hold_expires_at": booking.seat_hold_expires_at,
        "created_at": booking.created_at,
        "flight": {
            "id": booking.flight.id,
            "flight_number": booking.flight.flight_number,
            "scheduled_departure": booking.flight.scheduled_departure,
            "scheduled_arrival": booking.flight.scheduled_arrival
        },
        "tickets": [
            {
                "id": t.id,
                "ticket_number": t.ticket_number,
                "seat_number": t.seat_number
            }
            for t in tickets
        ]
    }


@router.get("/bookings/upcoming", response_model=List[BookingDetailResponse])
def get_upcoming_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Get upcoming trips"""
    bookings = get_user_bookings(db, current_user.id, upcoming_only=True)
    result = []
    for booking in bookings:
        payment = db.query(Payment).filter(Payment.booking_id == booking.id).first()
        tickets = db.query(Ticket).filter(Ticket.booking_id == booking.id).all()
        result.append({
            "id": booking.id,
            "pnr": booking.pnr,
            "user_id": booking.user_id,
            "flight_id": booking.flight_id,
            "status": booking.status,
            "seat_hold_expires_at": booking.seat_hold_expires_at,
            "created_at": booking.created_at,
            "flight": {
                "id": booking.flight.id,
                "flight_number": booking.flight.flight_number,
                "scheduled_departure": booking.flight.scheduled_departure,
                "scheduled_arrival": booking.flight.scheduled_arrival
            },
            "tickets": [
                {
                    "id": t.id,
                    "ticket_number": t.ticket_number,
                    "seat_number": t.seat_number
                }
                for t in tickets
            ],
            "payment": {
                "id": payment.id,
                "amount": payment.amount,
                "status": payment.status
            } if payment else None
        })
    return result


@router.get("/bookings/past", response_model=List[BookingDetailResponse])
def get_past_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Get past trips"""
    bookings = get_user_bookings(db, current_user.id, upcoming_only=False)
    result = []
    for booking in bookings:
        payment = db.query(Payment).filter(Payment.booking_id == booking.id).first()
        tickets = db.query(Ticket).filter(Ticket.booking_id == booking.id).all()
        result.append({
            "id": booking.id,
            "pnr": booking.pnr,
            "user_id": booking.user_id,
            "flight_id": booking.flight_id,
            "status": booking.status,
            "seat_hold_expires_at": booking.seat_hold_expires_at,
            "created_at": booking.created_at,
            "flight": {
                "id": booking.flight.id,
                "flight_number": booking.flight.flight_number,
                "scheduled_departure": booking.flight.scheduled_departure,
                "scheduled_arrival": booking.flight.scheduled_arrival
            },
            "tickets": [
                {
                    "id": t.id,
                    "ticket_number": t.ticket_number,
                    "seat_number": t.seat_number
                }
                for t in tickets
            ],
            "payment": {
                "id": payment.id,
                "amount": payment.amount,
                "status": payment.status
            } if payment else None
        })
    return result


@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment_endpoint(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Process payment for a booking (mock payment)"""
    return process_payment(db, payment_data.booking_id, payment_data.transaction_id)


@router.post("/check-in/{ticket_id}", response_model=CheckInResponse)
def check_in_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Check in for a flight (24h-1h before departure)"""
    checkin = check_in(db, ticket_id, current_user.id)
    
    # Get ticket and flight info
    from app.models.ticket import Ticket
    from app.models.booking import Booking
    
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    booking = db.query(Booking).filter(Booking.id == ticket.booking_id).first()
    flight = booking.flight
    
    return {
        "id": checkin.id,
        "ticket_id": checkin.ticket_id,
        "qr_code": checkin.qr_code,
        "checked_in_at": checkin.checked_in_at,
        "ticket": {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "seat_number": ticket.seat_number
        },
        "flight": {
            "id": flight.id,
            "flight_number": flight.flight_number,
            "scheduled_departure": flight.scheduled_departure
        }
    }


@router.get("/announcements", response_model=List[AnnouncementResponse])
def get_announcements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_passenger)
):
    """Get announcements for user's upcoming flights"""
    from app.models.booking import Booking
    from app.models.ticket import Ticket
    
    # Get user's upcoming bookings
    bookings = get_user_bookings(db, current_user.id, upcoming_only=True)
    flight_ids = [b.flight_id for b in bookings]
    
    if not flight_ids:
        return []
    
    announcements = db.query(Announcement).filter(
        Announcement.flight_id.in_(flight_ids)
    ).order_by(Announcement.created_at.desc()).all()
    
    result = []
    for ann in announcements:
        result.append({
            "id": ann.id,
            "flight_id": ann.flight_id,
            "announcement_type": ann.announcement_type,
            "message": ann.message,
            "created_at": ann.created_at,
            "flight": {
                "id": ann.flight.id,
                "flight_number": ann.flight.flight_number
            }
        })
    return result


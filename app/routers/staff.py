from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_staff
from app.models.user import User
from app.models.airplane import Airplane
from app.models.flight import Flight
from app.models.booking import Booking
from app.models.announcement import Announcement
from app.schemas.airplane import AirplaneCreate, AirplaneResponse
from app.schemas.flight import FlightCreate, FlightUpdate, FlightResponse
from app.schemas.announcement import AnnouncementCreate, AnnouncementResponse
from app.schemas.booking import BookingResponse

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/airplanes", response_model=AirplaneResponse, status_code=status.HTTP_201_CREATED)
def create_airplane(
    airplane_data: AirplaneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Create a new airplane"""
    airplane = Airplane(**airplane_data.dict())
    db.add(airplane)
    db.commit()
    db.refresh(airplane)
    return airplane


@router.get("/airplanes", response_model=List[AirplaneResponse])
def list_airplanes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """List all airplanes"""
    return db.query(Airplane).all()


@router.post("/flights", response_model=FlightResponse, status_code=status.HTTP_201_CREATED)
def create_flight(
    flight_data: FlightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Create a new flight"""
    flight = Flight(**flight_data.dict())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight


@router.get("/flights", response_model=List[FlightResponse])
def list_flights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """List all flights"""
    return db.query(Flight).all()


@router.get("/flights/{flight_id}", response_model=FlightResponse)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Get flight details"""
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    return flight


@router.put("/flights/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight_data: FlightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Update a flight"""
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    for key, value in flight_data.dict(exclude_unset=True).items():
        setattr(flight, key, value)
    
    db.commit()
    db.refresh(flight)
    return flight


@router.post("/announcements", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Create an announcement for a flight"""
    # Verify flight exists
    flight = db.query(Flight).filter(Flight.id == announcement_data.flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    announcement = Announcement(**announcement_data.dict())
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    
    return {
        "id": announcement.id,
        "flight_id": announcement.flight_id,
        "announcement_type": announcement.announcement_type,
        "message": announcement.message,
        "created_at": announcement.created_at,
        "flight": {
            "id": flight.id,
            "flight_number": flight.flight_number
        }
    }


@router.get("/bookings", response_model=List[BookingResponse])
def list_bookings(
    flight_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """List all bookings (optionally filtered by flight)"""
    query = db.query(Booking)
    if flight_id:
        query = query.filter(Booking.flight_id == flight_id)
    bookings = query.all()
    
    result = []
    for booking in bookings:
        from app.models.ticket import Ticket
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
                "flight_number": booking.flight.flight_number
            },
            "tickets": [
                {
                    "id": t.id,
                    "ticket_number": t.ticket_number,
                    "seat_number": t.seat_number
                }
                for t in tickets
            ]
        })
    return result


@router.post("/bookings/{booking_id}/cancel")
def cancel_booking_staff(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Cancel a booking (staff only)"""
    from app.services.booking_service import cancel_booking
    return cancel_booking(db, booking_id)


@router.put("/bookings/{booking_id}/reassign-seat")
def reassign_seat(
    booking_id: int,
    ticket_id: int,
    new_seat: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    """Reassign a seat for a ticket"""
    from app.models.ticket import Ticket
    from app.models.booking import Booking, BookingStatus
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.booking_id == booking_id
    ).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Check if new seat is available
    booked_seats = set()
    for t in db.query(Ticket).join(Booking).filter(
        Booking.flight_id == booking.flight_id,
        Booking.status != BookingStatus.CANCELLED,
        Ticket.id != ticket_id
    ).all():
        booked_seats.add(t.seat_number)
    
    if new_seat in booked_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Seat {new_seat} is already booked"
        )
    
    ticket.seat_number = new_seat
    db.commit()
    db.refresh(ticket)
    
    return {
        "message": "Seat reassigned successfully",
        "ticket": {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "seat_number": ticket.seat_number
        }
    }


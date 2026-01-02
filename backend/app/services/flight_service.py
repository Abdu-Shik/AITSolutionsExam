from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from app.models.flight import Flight
from app.models.airport import Airport
from app.models.ticket import Ticket
from app.models.booking import Booking, BookingStatus
from app.schemas.flight import FlightSearch


def search_flights(
    db: Session,
    search_params: FlightSearch
) -> list:
    query = db.query(Flight)
    
    if search_params.origin:
        origin_airport = db.query(Airport).filter(
            Airport.code == search_params.origin.upper()
        ).first()
        if origin_airport:
            query = query.filter(Flight.origin_id == origin_airport.id)
    
    if search_params.destination:
        dest_airport = db.query(Airport).filter(
            Airport.code == search_params.destination.upper()
        ).first()
        if dest_airport:
            query = query.filter(Flight.destination_id == dest_airport.id)
    
    if search_params.date:
        # Search for flights on the given date
        start_date = search_params.date.replace(hour=0, minute=0, second=0)
        end_date = start_date + timedelta(days=1)
        query = query.filter(
            Flight.scheduled_departure >= start_date,
            Flight.scheduled_departure < end_date
        )
    
    return query.all()


def get_flight_details(db: Session, flight_id: int) -> dict:
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    # Get booked seats
    booked_seats = set()
    for ticket in db.query(Ticket).join(Booking).filter(
        Booking.flight_id == flight_id,
        Booking.status != BookingStatus.CANCELLED
    ).all():
        booked_seats.add(ticket.seat_number)
    
    # Get available seats
    total_seats = flight.airplane.total_seats
    available_seats = total_seats - len(booked_seats)
    
    return {
        "flight": flight,
        "available_seats": available_seats,
        "total_seats": total_seats,
        "booked_seats": list(booked_seats)
    }


def get_seat_map(db: Session, flight_id: int) -> dict:
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    # Get booked seats
    booked_seats = set()
    for ticket in db.query(Ticket).join(Booking).filter(
        Booking.flight_id == flight_id,
        Booking.status != BookingStatus.CANCELLED
    ).all():
        booked_seats.add(ticket.seat_number)
    
    seat_template = flight.airplane.seat_template
    rows = seat_template.get("rows", 30)
    seats_per_row = seat_template.get("seats_per_row", 6)
    layout = seat_template.get("layout", "3-3")
    
    # Generate seat map
    seat_map = []
    seat_letters = "ABCDEFGH"
    
    for row in range(1, rows + 1):
        row_seats = []
        for col in range(seats_per_row):
            seat_letter = seat_letters[col]
            seat_number = f"{row}{seat_letter}"
            row_seats.append({
                "seat": seat_number,
                "available": seat_number not in booked_seats
            })
        seat_map.append(row_seats)
    
    return {
        "seat_map": seat_map,
        "layout": layout,
        "total_seats": flight.airplane.total_seats,
        "available_seats": flight.airplane.total_seats - len(booked_seats)
    }


"""
Seed script to populate initial data for airports, airplanes, and flights
Run this script after initial setup to populate the database with sample data
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.airport import Airport
from app.models.airplane import Airplane
from app.models.flight import Flight, FlightStatus
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


def seed_airports():
    """Seed airports"""
    airports_data = [
        {"code": "JFK", "name": "John F. Kennedy International Airport", "city": "New York", "country": "USA"},
        {"code": "LAX", "name": "Los Angeles International Airport", "city": "Los Angeles", "country": "USA"},
        {"code": "LHR", "name": "Heathrow Airport", "city": "London", "country": "UK"},
        {"code": "CDG", "name": "Charles de Gaulle Airport", "city": "Paris", "country": "France"},
        {"code": "DXB", "name": "Dubai International Airport", "city": "Dubai", "country": "UAE"},
        {"code": "SIN", "name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore"},
        {"code": "NRT", "name": "Narita International Airport", "city": "Tokyo", "country": "Japan"},
        {"code": "SYD", "name": "Sydney Kingsford Smith Airport", "city": "Sydney", "country": "Australia"},
    ]
    
    for airport_data in airports_data:
        existing = db.query(Airport).filter(Airport.code == airport_data["code"]).first()
        if not existing:
            airport = Airport(**airport_data)
            db.add(airport)
    
    db.commit()
    print("[OK] Airports seeded")


def seed_airplanes():
    """Seed airplanes"""
    airplanes_data = [
        {
            "model": "Boeing 737-800",
            "registration_number": "N123AB",
            "seat_template": {"rows": 30, "seats_per_row": 6, "layout": "3-3"},
            "total_seats": 180
        },
        {
            "model": "Airbus A320",
            "registration_number": "N456CD",
            "seat_template": {"rows": 28, "seats_per_row": 6, "layout": "3-3"},
            "total_seats": 168
        },
        {
            "model": "Boeing 777-300ER",
            "registration_number": "N789EF",
            "seat_template": {"rows": 42, "seats_per_row": 9, "layout": "3-3-3"},
            "total_seats": 378
        },
        {
            "model": "Airbus A350",
            "registration_number": "N321GH",
            "seat_template": {"rows": 40, "seats_per_row": 9, "layout": "3-3-3"},
            "total_seats": 360
        },
    ]
    
    for airplane_data in airplanes_data:
        existing = db.query(Airplane).filter(
            Airplane.registration_number == airplane_data["registration_number"]
        ).first()
        if not existing:
            airplane = Airplane(**airplane_data)
            db.add(airplane)
    
    db.commit()
    print("[OK] Airplanes seeded")


def seed_flights():
    """Seed flights"""
    # Get airports
    jfk = db.query(Airport).filter(Airport.code == "JFK").first()
    lax = db.query(Airport).filter(Airport.code == "LAX").first()
    lhr = db.query(Airport).filter(Airport.code == "LHR").first()
    cdg = db.query(Airport).filter(Airport.code == "CDG").first()
    
    # Get airplanes
    airplane1 = db.query(Airplane).filter(Airplane.registration_number == "N123AB").first()
    airplane2 = db.query(Airplane).filter(Airplane.registration_number == "N456CD").first()
    
    if not all([jfk, lax, lhr, cdg, airplane1, airplane2]):
        print("[WARNING] Required airports/airplanes not found. Please seed them first.")
        return
    
    # Create flights for the next 30 days
    flights_data = []
    base_date = datetime.utcnow().replace(hour=8, minute=0, second=0, microsecond=0)
    
    for day in range(30):
        flight_date = base_date + timedelta(days=day)
        
        # JFK to LAX
        flights_data.append({
            "flight_number": f"AA{100 + day}",
            "origin_id": jfk.id,
            "destination_id": lax.id,
            "airplane_id": airplane1.id,
            "scheduled_departure": flight_date,
            "scheduled_arrival": flight_date + timedelta(hours=6),
            "gate": "A12",
            "terminal": "1",
            "status": FlightStatus.SCHEDULED
        })
        
        # LAX to JFK
        flights_data.append({
            "flight_number": f"AA{200 + day}",
            "origin_id": lax.id,
            "destination_id": jfk.id,
            "airplane_id": airplane1.id,
            "scheduled_departure": flight_date + timedelta(hours=2),
            "scheduled_arrival": flight_date + timedelta(hours=8),
            "gate": "B5",
            "terminal": "2",
            "status": FlightStatus.SCHEDULED
        })
        
        # LHR to CDG
        flights_data.append({
            "flight_number": f"BA{300 + day}",
            "origin_id": lhr.id,
            "destination_id": cdg.id,
            "airplane_id": airplane2.id,
            "scheduled_departure": flight_date + timedelta(hours=4),
            "scheduled_arrival": flight_date + timedelta(hours=5, minutes=30),
            "gate": "C8",
            "terminal": "3",
            "status": FlightStatus.SCHEDULED
        })
    
    for flight_data in flights_data:
        existing = db.query(Flight).filter(
            Flight.flight_number == flight_data["flight_number"]
        ).first()
        if not existing:
            flight = Flight(**flight_data)
            db.add(flight)
    
    db.commit()
    print("[OK] Flights seeded")


def seed_admin_user():
    """Seed admin/staff user"""
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@airline.com",
            hashed_password=get_password_hash("admin123"),
            role="staff",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("[OK] Admin user created (username: admin, password: admin123)")
    else:
        print("[OK] Admin user already exists")


if __name__ == "__main__":
    print("Seeding database...")
    seed_airports()
    seed_airplanes()
    seed_flights()
    seed_admin_user()
    print("\n[OK] Database seeding completed!")
    print("\nAdmin credentials:")
    print("  Username: admin")
    print("  Password: admin123")


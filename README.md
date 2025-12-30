# Airline Booking & Operations System

A comprehensive airline booking and operations management system built with FastAPI, SQLite, and JWT authentication.

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **SQLite** - Lightweight database with SQLAlchemy ORM
- **JWT** - JSON Web Token authentication
- **Pydantic** - Data validation
- **Swagger/OpenAPI** - Interactive API documentation at `/docs`

## Features

### Passenger Features
- User registration and login with JWT authentication
- Complete passenger profile management
- Search flights by origin, destination, and date
- View flight details and seat maps
- Book seats with 10-minute hold period
- Mock payment processing (idempotent)
- Manage trips (upcoming and past bookings)
- Check-in (24 hours to 1 hour before departure)
- Boarding pass with QR code
- Receive flight announcements

### Staff Features
- Manage airplanes and seat templates
- Create and update flights
- Assign airplanes, schedules, gates, and status
- Publish announcements (delay, cancellation, gate change, boarding)
- Manage bookings (view, cancel, reassign seats)

## Project Structure

```
AITSolutionsExam/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database connection and session
│   │   ├── security.py         # JWT and password hashing
│   │   └── dependencies.py     # FastAPI dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── passenger_profile.py
│   │   ├── airport.py
│   │   ├── airplane.py
│   │   ├── flight.py
│   │   ├── booking.py
│   │   ├── ticket.py
│   │   ├── payment.py
│   │   ├── checkin.py
│   │   └── announcement.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── passenger_profile.py
│   │   ├── airport.py
│   │   ├── airplane.py
│   │   ├── flight.py
│   │   ├── booking.py
│   │   ├── payment.py
│   │   ├── checkin.py
│   │   └── announcement.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── flight_service.py
│   │   ├── booking_service.py
│   │   ├── payment_service.py
│   │   └── checkin_service.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # Authentication endpoints
│       ├── passenger.py       # Passenger endpoints
│       └── staff.py           # Staff endpoints
├── seed_data.py               # Database seeding script
├── requirements.txt           # Python dependencies
├── instructions.txt           # Project requirements
└── README.md                  # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd AITSolutionsExam
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Seed the database with initial data**
   ```bash
   python seed_data.py
   ```
   This will create:
   - Sample airports (JFK, LAX, LHR, CDG, etc.)
   - Sample airplanes with seat configurations
   - Sample flights for the next 30 days
   - Admin user account

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at:
   - **API Base URL**: `http://localhost:8000`
   - **Interactive API Docs (Swagger)**: `http://localhost:8000/docs`
   - **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register a new user (passenger or staff)
- `POST /login` - Login and get JWT token
- `GET /me` - Get current user information
- `POST /profile` - Create/update passenger profile
- `GET /profile` - Get passenger profile

### Passenger Endpoints (`/api/v1/passenger`)
- `GET /flights/search` - Search flights
- `GET /flights/{flight_id}` - Get flight details
- `GET /flights/{flight_id}/seat-map` - Get seat map
- `POST /bookings` - Create a booking
- `GET /bookings/upcoming` - Get upcoming trips
- `GET /bookings/past` - Get past trips
- `POST /payments` - Process payment
- `POST /check-in/{ticket_id}` - Check in for flight
- `GET /announcements` - Get flight announcements

### Staff Endpoints (`/api/v1/staff`)
- `POST /airplanes` - Create airplane
- `GET /airplanes` - List all airplanes
- `POST /flights` - Create flight
- `GET /flights` - List all flights
- `GET /flights/{flight_id}` - Get flight details
- `PUT /flights/{flight_id}` - Update flight
- `POST /announcements` - Create announcement
- `GET /bookings` - List bookings
- `POST /bookings/{booking_id}/cancel` - Cancel booking
- `PUT /bookings/{booking_id}/reassign-seat` - Reassign seat

## Admin Credentials

After running `seed_data.py`, you can use these credentials to login as staff:

- **Username**: `admin`
- **Password**: `admin123`

## Usage Examples

### 1. Register a Passenger
```bash
POST http://localhost:8000/api/v1/auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "passenger"
}
```

### 2. Login
```bash
POST http://localhost:8000/api/v1/auth/login
{
  "username": "john_doe",
  "password": "password123"
}
```

Response includes `access_token` - use this in the Authorization header:
```
Authorization: Bearer <access_token>
```

### 3. Complete Passenger Profile
```bash
POST http://localhost:8000/api/v1/auth/profile
Authorization: Bearer <access_token>
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "passport_number": "AB123456",
  "nationality": "USA",
  "date_of_birth": "1990-01-01"
}
```

### 4. Search Flights
```bash
GET http://localhost:8000/api/v1/passenger/flights/search?origin=JFK&destination=LAX&date=2024-01-15T00:00:00
Authorization: Bearer <access_token>
```

### 5. Create Booking
```bash
POST http://localhost:8000/api/v1/passenger/bookings
Authorization: Bearer <access_token>
{
  "flight_id": 1,
  "passenger_profiles": [
    {
      "passenger_profile_id": 1,
      "seat_number": "12A"
    }
  ]
}
```

### 6. Process Payment
```bash
POST http://localhost:8000/api/v1/passenger/payments
Authorization: Bearer <access_token>
{
  "booking_id": 1,
  "transaction_id": "TXN123456789"
}
```

## Database

The application uses SQLite database (`airline.db`) which is created automatically on first run. The database file will be created in the project root directory.

To reset the database:
1. Delete `airline.db` file
2. Run `python seed_data.py` again

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation with try-it-out functionality
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation

## Notes

- All payments are **mock payments** - they always succeed
- Seat holds expire after **10 minutes**
- Check-in is available **24 hours to 1 hour** before departure
- JWT tokens expire after **30 minutes** (configurable in `app/core/config.py`)
- The system prevents double booking of seats
- All endpoints require authentication except `/register` and `/login`

## Development

To run in development mode with auto-reload:
```bash
uvicorn app.main:app --reload
```

## License

This project is part of AIT Solutions Exam.

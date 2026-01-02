# Airline System - Backend API

This directory contains the FastAPI backend for the Airline Booking & Operations System.

## Tech Stack
- **Python 3.10+**
- **FastAPI**: Web framework
- **SQLite**: Database (via SQLAlchemy)
- **JWT**: Authentication
- **Uvicorn**: ASGI Server

## Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- Pip

### 2. Installation
Open a terminal in this `backend` directory:

```bash
# Optional: Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
The project uses SQLite. To create the database and populate it with sample data (Airports, Flights, Admin User):

```bash
python seed_data.py
```
This creates `airline.db` in this folder.

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

## How to Run

Start the server from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

### Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
- `app/`: Main application code
  - `routers/`: API endpoints (auth, passenger, staff)
  - `models/`: Database models
  - `core/`: Config and database connection
- `requirements.txt`: Dependencies
- `seed_data.py`: Script to populate database

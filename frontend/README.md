# Airline System - Flutter Frontend

This directory contains the Flutter mobile application for the Airline Booking System.

## Tech Stack
- **Flutter SDK** (Dart)
- **Provider**: State Management
- **http**: API calls
- **shared_preferences**: Local storage (JWT)

## Setup Instructions

### 1. Prerequisites
- Flutter SDK installed and in PATH
- Android Studio / VS Code with Flutter extensions
- Android Emulator or Physical Device

### 2. Install Dependencies
Navigate to the `frontend` directory and run:

```bash
flutter pub get
```

## Configuration
The app connects to the FastAPI backend. The API URL is configured in `lib/config.dart`.

```dart
class Config {
  static String get baseUrl {
    if (Platform.isAndroid) {
      // 10.0.2.2 is the special alias to localhost for Android Emulators
      return 'http://10.0.2.2:8000/api/v1';
    }
    // For iOS or Desktop runs
    return 'http://127.0.0.1:8000/api/v1';
  }
}
```
**Note:** If using a physical device, change the URL to your computer's local IP address (e.g., `http://192.168.1.5:8000/api/v1`).

## How to Run

1.  **Ensure the Backend is Running**:
    See `../backend/README.md` for instructions.

2.  **Start the App**:
    ```bash
    flutter run
    ```

## Features
- **Login/Register**: Connected to backend Auth API.
- **Flight Search**: Search by origin/destination.
- **Booking**: Book tickets (stored in backend).
- **My Trips**: View upcoming and past flights.
- **Check-in**: Generate QR codes for boarding.

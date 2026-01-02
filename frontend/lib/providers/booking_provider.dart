import 'package:flutter/material.dart';
import '../services/booking_service.dart';
import '../models/booking.dart';
import '../models/passenger_profile.dart';

class BookingProvider with ChangeNotifier {
  final BookingService _bookingService = BookingService();
  List<Booking> _upcomingBookings = [];
  List<Booking> _pastBookings = [];
  bool _isLoading = false;

  List<Booking> get upcomingBookings => _upcomingBookings;
  List<Booking> get pastBookings => _pastBookings;
  bool get isLoading => _isLoading;

  Future<void> loadBookings() async {
    _isLoading = true;
    notifyListeners();
    try {
      _upcomingBookings = await _bookingService.getUpcomingBookings();
      _pastBookings = await _bookingService.getPastBookings();
    } catch (e) {
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Booking> createBooking(int flightId, List<PassengerProfile> passengers) async {
    return await _bookingService.createBooking(flightId, passengers);
  }

  Future<Map<String, dynamic>> checkIn(int ticketId) async {
    return await _bookingService.checkIn(ticketId);
  }
}

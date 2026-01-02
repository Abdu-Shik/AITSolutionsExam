import 'api_service.dart';
import '../models/booking.dart';
import '../models/passenger_profile.dart';

class BookingService extends ApiService {
  Future<Booking> createBooking(int flightId, List<PassengerProfile> passengers) async {
    final response = await post('/passenger/bookings', body: {
      'flight_id': flightId,
      'passenger_profiles': passengers.map((p) => p.toJson()).toList(),
    });
    return Booking.fromJson(response);
  }

  Future<List<Booking>> getUpcomingBookings() async {
    final List<dynamic> json = await get('/passenger/bookings/upcoming');
    return json.map((e) => Booking.fromJson(e)).toList();
  }

  Future<List<Booking>> getPastBookings() async {
    final List<dynamic> json = await get('/passenger/bookings/past');
    return json.map((e) => Booking.fromJson(e)).toList();
  }

  Future<Map<String, dynamic>> checkIn(int ticketId) async {
    return await post('/passenger/check-in/$ticketId');
  }
}

import 'api_service.dart';
import '../models/flight.dart';

class FlightService extends ApiService {
  Future<List<Flight>> searchFlights(String? origin, String? destination, String? date) async {
    String query = '/passenger/flights/search?';
    if (origin != null && origin.isNotEmpty) query += 'origin=$origin&';
    if (destination != null && destination.isNotEmpty) query += 'destination=$destination&';
    if (date != null && date.isNotEmpty) query += 'date=$date&';

    final List<dynamic> json = await get(query);
    return json.map((e) => Flight.fromJson(e)).toList();
  }

  Future<Map<String, dynamic>> getFlightDetails(int id) async {
    return await get('/passenger/flights/$id');
  }
}

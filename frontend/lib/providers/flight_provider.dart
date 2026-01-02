import 'package:flutter/material.dart';
import '../services/flight_service.dart';
import '../models/flight.dart';

class FlightProvider with ChangeNotifier {
  final FlightService _flightService = FlightService();
  List<Flight> _searchResults = [];
  bool _isLoading = false;

  List<Flight> get searchResults => _searchResults;
  bool get isLoading => _isLoading;

  Future<void> searchFlights(String? origin, String? destination, String? date) async {
    _isLoading = true;
    notifyListeners();
    try {
      _searchResults = await _flightService.searchFlights(origin, destination, date);
    } catch (e) {
      _searchResults = [];
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>> getFlightDetails(int id) async {
    return await _flightService.getFlightDetails(id);
  }
}

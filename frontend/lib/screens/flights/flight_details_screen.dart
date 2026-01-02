import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/flight_provider.dart';
import '../booking/booking_screen.dart';

class FlightDetailsScreen extends StatefulWidget {
  final int flightId;
  const FlightDetailsScreen({super.key, required this.flightId});

  @override
  State<FlightDetailsScreen> createState() => _FlightDetailsScreenState();
}

class _FlightDetailsScreenState extends State<FlightDetailsScreen> {
  Map<String, dynamic>? _details;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadDetails();
  }

  Future<void> _loadDetails() async {
    try {
      final data = await Provider.of<FlightProvider>(context, listen: false)
          .getFlightDetails(widget.flightId);
      setState(() {
        _details = data;
        _loading = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    if (_details == null) return const Scaffold(body: Center(child: Text('Error loading details')));

    final flight = _details!;
    final airplane = flight['airplane'];
    final availableSeats = flight['available_seats'] as List;

    return Scaffold(
      appBar: AppBar(title: Text(flight['flight_number'])),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('From: ${flight['origin_airport']['city']}', style: Theme.of(context).textTheme.titleLarge),
            Text('To: ${flight['destination_airport']['city']}', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 10),
            Text('Date: ${flight['scheduled_departure']}'),
            Text('Gate: ${flight['gate'] ?? "TBD"}'),
            Text('Aircraft: ${airplane['model']}'),
            const SizedBox(height: 20),
            Text('Available Seats: ${availableSeats.length}'),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => BookingScreen(flightData: flight),
                    ),
                  );
                },
                child: const Text('Book This Flight'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/flight_provider.dart';
import '../../models/flight.dart';
import 'flight_details_screen.dart';

class FlightResultsScreen extends StatelessWidget {
  const FlightResultsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final flights = Provider.of<FlightProvider>(context).searchResults;
    final isLoading = Provider.of<FlightProvider>(context).isLoading;

    return Scaffold(
      appBar: AppBar(title: const Text('Flight Results')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : flights.isEmpty
              ? const Center(child: Text('No flights found'))
              : ListView.builder(
                  itemCount: flights.length,
                  itemBuilder: (context, index) {
                    final flight = flights[index];
                    return Card(
                      child: ListTile(
                        title: Text('${flight.originAirport.city} (${flight.originAirport.code}) -> ${flight.destinationAirport.city} (${flight.destinationAirport.code})'),
                        subtitle: Text('Flight: ${flight.flightNumber}\nDep: ${flight.scheduledDeparture}'),
                        trailing: const Icon(Icons.arrow_forward),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => FlightDetailsScreen(flightId: flight.id),
                            ),
                          );
                        },
                      ),
                    );
                  },
                ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/booking_provider.dart';
import '../checkin/checkin_screen.dart';

class TripsScreen extends StatefulWidget {
  const TripsScreen({super.key});

  @override
  State<TripsScreen> createState() => _TripsScreenState();
}

class _TripsScreenState extends State<TripsScreen> {
  @override
  void initState() {
    super.initState();
    // Load bookings when screen opens
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<BookingProvider>(context, listen: false).loadBookings();
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BookingProvider>(context);

    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('My Trips'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Upcoming'),
              Tab(text: 'Past'),
            ],
          ),
        ),
        body: provider.isLoading
            ? const Center(child: CircularProgressIndicator())
            : TabBarView(
                children: [
                  _buildList(context, provider.upcomingBookings, isUpcoming: true),
                  _buildList(context, provider.pastBookings, isUpcoming: false),
                ],
              ),
      ),
    );
  }

  Widget _buildList(BuildContext context, List bookings, {required bool isUpcoming}) {
    if (bookings.isEmpty) return const Center(child: Text('No trips found'));
    return ListView.builder(
      itemCount: bookings.length,
      itemBuilder: (context, index) {
        final booking = bookings[index];
        final flight = booking.flight;
        return Card(
          child: ExpansionTile(
            title: Text('${flight.originAirport.code} -> ${flight.destinationAirport.code}'),
            subtitle: Text('Date: ${flight.scheduledDeparture}\nPNR: ${booking.pnr}'),
            children: [
              if (isUpcoming && booking.tickets.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.qr_code),
                    label: const Text('Check-in / Boarding Pass'),
                    onPressed: () {
                      // Just take the first ticket for demo
                      final ticketId = booking.tickets.first.id;
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => CheckInScreen(ticketId: ticketId),
                        ),
                      );
                    },
                  ),
                )
            ],
          ),
        );
      },
    );
  }
}

import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:provider/provider.dart';
import '../../providers/booking_provider.dart';

class CheckInScreen extends StatefulWidget {
  final int ticketId;
  const CheckInScreen({super.key, required this.ticketId});

  @override
  State<CheckInScreen> createState() => _CheckInScreenState();
}

class _CheckInScreenState extends State<CheckInScreen> {
  Map<String, dynamic>? _checkInData;
  bool _loading = false;
  bool _checkedIn = false;

  Future<void> _doCheckIn() async {
    setState(() => _loading = true);
    try {
      final result = await Provider.of<BookingProvider>(context, listen: false)
          .checkIn(widget.ticketId);
      setState(() {
        _checkInData = result;
        _checkedIn = true;
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Verification Failed (Too early?): $e')),
      );
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Boarding Pass')),
      body: Center(
        child: _loading 
            ? const CircularProgressIndicator()
            : _checkedIn && _checkInData != null
                ? Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Scan this at the gate', style: TextStyle(fontSize: 18)),
                      const SizedBox(height: 20),
                      QrImageView(
                        data: _checkInData!['qr_code'],
                        version: QrVersions.auto,
                        size: 200.0,
                      ),
                      const SizedBox(height: 20),
                      Text('Seat: ${_checkInData!['ticket']['seat_number']}'),
                      Text('Flight: ${_checkInData!['flight']['flight_number']}'),
                    ],
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Ready to fly?'),
                      const SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: _doCheckIn,
                        child: const Text('Check In Now'),
                      ),
                    ],
                  ),
      ),
    );
  }
}

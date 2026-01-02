import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/flight_provider.dart';
import 'flight_results_screen.dart';

class FlightSearchScreen extends StatefulWidget {
  const FlightSearchScreen({super.key});

  @override
  State<FlightSearchScreen> createState() => _FlightSearchScreenState();
}

class _FlightSearchScreenState extends State<FlightSearchScreen> {
  final _originController = TextEditingController();
  final _destinationController = TextEditingController();
  DateTime? _selectedDate;

  Future<void> _search() async {
    try {
      String? dateStr;
      if (_selectedDate != null) {
        dateStr = _selectedDate!.toIso8601String().split('T')[0];
      }
      
      await Provider.of<FlightProvider>(context, listen: false).searchFlights(
        _originController.text,
        _destinationController.text,
        dateStr,
      );
      
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => const FlightResultsScreen()),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Search Failed: ${e.toString()}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          TextField(
            controller: _originController,
            decoration: const InputDecoration(labelText: 'From (City/Code)'),
          ),
          TextField(
            controller: _destinationController,
            decoration: const InputDecoration(labelText: 'To (City/Code)'),
          ),
          ListTile(
            title: Text(_selectedDate == null 
              ? 'Select Date' 
              : 'Date: ${_selectedDate.toString().split(' ')[0]}'),
            trailing: const Icon(Icons.calendar_today),
            onTap: () async {
              final picked = await showDatePicker(
                context: context,
                initialDate: DateTime.now(),
                firstDate: DateTime.now(),
                lastDate: DateTime.now().add(const Duration(days: 365)),
              );
              if (picked != null) {
                setState(() => _selectedDate = picked);
              }
            },
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _search,
            child: const Text('Search Flights'),
          ),
        ],
      ),
    );
  }
}

class Airport {
  final int id;
  final String code;
  final String name;
  final String city;
  final String country;

  Airport({
    required this.id,
    required this.code,
    required this.name,
    required this.city,
    required this.country,
  });

  factory Airport.fromJson(Map<String, dynamic> json) {
    return Airport(
      id: json['id'],
      code: json['code'],
      name: json['name'],
      city: json['city'],
      country: json['country'],
    );
  }
}

class Flight {
  final int id;
  final String flightNumber;
  final String scheduledDeparture;
  final String scheduledArrival;
  final String status;
  final Airport originAirport;
  final Airport destinationAirport;

  Flight({
    required this.id,
    required this.flightNumber,
    required this.scheduledDeparture,
    required this.scheduledArrival,
    required this.status,
    required this.originAirport,
    required this.destinationAirport,
  });

  factory Flight.fromJson(Map<String, dynamic> json) {
    return Flight(
      id: json['id'],
      flightNumber: json['flight_number'],
      scheduledDeparture: json['scheduled_departure'],
      scheduledArrival: json['scheduled_arrival'],
      status: json['status'],
      originAirport: Airport.fromJson(json['origin_airport']),
      destinationAirport: Airport.fromJson(json['destination_airport']),
    );
  }

  DateTime get departureTime => DateTime.parse(scheduledDeparture);
  DateTime get arrivalTime => DateTime.parse(scheduledArrival);
}

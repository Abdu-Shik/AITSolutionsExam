import 'flight.dart';

class Ticket {
  final int id;
  final String ticketNumber;
  final String seatNumber;

  Ticket({
    required this.id,
    required this.ticketNumber,
    required this.seatNumber,
  });

  factory Ticket.fromJson(Map<String, dynamic> json) {
    return Ticket(
      id: json['id'],
      ticketNumber: json['ticket_number'],
      seatNumber: json['seat_number'],
    );
  }
}

class Booking {
  final int id;
  final String pnr;
  final String status;
  final Flight flight;
  final List<Ticket> tickets;

  Booking({
    required this.id,
    required this.pnr,
    required this.status,
    required this.flight,
    required this.tickets,
  });

  factory Booking.fromJson(Map<String, dynamic> json) {
    return Booking(
      id: json['id'],
      pnr: json['pnr'],
      status: json['status'],
      flight: Flight.fromJson(json['flight']),
      tickets: (json['tickets'] as List?)
          ?.map((t) => Ticket.fromJson(t))
          .toList() ?? [],
    );
  }
}

class PassengerProfile {
  final int id;
  final String firstName;
  final String lastName;
  final String passportNumber;
  final String nationality;
  final String dateOfBirth;

  PassengerProfile({
    required this.id,
    required this.firstName,
    required this.lastName,
    required this.passportNumber,
    required this.nationality,
    required this.dateOfBirth,
  });

  factory PassengerProfile.fromJson(Map<String, dynamic> json) {
    return PassengerProfile(
      id: json['id'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      passportNumber: json['passport_number'],
      nationality: json['nationality'],
      dateOfBirth: json['date_of_birth'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'first_name': firstName,
      'last_name': lastName,
      'passport_number': passportNumber,
      'nationality': nationality,
      'date_of_birth': dateOfBirth,
    };
  }
}

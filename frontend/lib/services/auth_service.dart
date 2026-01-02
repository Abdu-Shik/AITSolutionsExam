import 'api_service.dart';
import '../models/user.dart';
import '../models/passenger_profile.dart';

class AuthService extends ApiService {
  Future<dynamic> login(String username, String password) async {
    return await post('/auth/login', body: {
      'username': username,
      'password': password,
    }, auth: false);
  }

  Future<dynamic> register(String email, String username, String password) async {
    return await post('/auth/register', body: {
      'email': email,
      'username': username,
      'password': password,
      'role': 'passenger',
    }, auth: false);
  }

  Future<User> getCurrentUser() async {
    final json = await get('/auth/me');
    return User.fromJson(json);
  }

  Future<PassengerProfile?> getProfile() async {
    try {
      final json = await get('/auth/profile');
      return PassengerProfile.fromJson(json);
    } catch (e) {
      return null;
    }
  }

  Future<PassengerProfile> createProfile(PassengerProfile profile) async {
    final json = await post('/auth/profile', body: profile.toJson());
    return PassengerProfile.fromJson(json);
  }
}

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/auth_service.dart';
import '../models/user.dart';
import '../models/passenger_profile.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  User? _user;
  PassengerProfile? _profile;
  bool _isAuthenticated = false;
  bool _isLoading = false;

  User? get user => _user;
  PassengerProfile? get profile => _profile;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;

  Future<void> checkAuth() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token != null) {
      try {
        _user = await _authService.getCurrentUser();
        try {
          _profile = await _authService.getProfile();
        } catch (_) {} 
        _isAuthenticated = true;
      } catch (e) {
        _isAuthenticated = false;
        await prefs.remove('access_token');
      }
    }
    notifyListeners();
  }

  Future<void> login(String username, String password) async {
    _isLoading = true;
    notifyListeners();
    try {
      final response = await _authService.login(username, password);
      final token = response['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', token);
      
      _user = await _authService.getCurrentUser();
      try {
        _profile = await _authService.getProfile();
      } catch (_) {}
      
      _isAuthenticated = true;
    } catch (e) {
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> register(String email, String username, String password) async {
    _isLoading = true;
    notifyListeners();
    try {
      await _authService.register(email, username, password);
    } catch (e) {
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> createProfile(PassengerProfile profile) async {
    _isLoading = true;
    notifyListeners();
    try {
      _profile = await _authService.createProfile(profile);
    } catch (e) {
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    _user = null;
    _profile = null;
    _isAuthenticated = false;
    notifyListeners();
  }
}

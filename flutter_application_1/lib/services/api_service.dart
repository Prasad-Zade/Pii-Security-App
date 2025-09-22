import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart';
import '../models/chat_session.dart';
import 'local_storage_service.dart';

class ApiService {
  static const String baseUrl = 'https://pii-security-app.onrender.com/api';

  // Session management
  static Future<List<ChatSession>> getSessions() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/sessions'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final sessions = (data['data'] as List)
            .map((json) => ChatSession.fromJson(json))
            .toList();
        await LocalStorageService.saveSessions(sessions);
        return sessions;
      }
    } catch (_) {}
    return await LocalStorageService.getSessions();
  }

  static Future<ChatSession> createSession({String title = 'New Chat'}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/sessions'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'title': title}),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final session = ChatSession.fromJson(data['data']);
        await LocalStorageService.addSession(session);
        return session;
      }
    } catch (_) {}
    
    final session = ChatSession(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
    await LocalStorageService.addSession(session);
    return session;
  }

  static Future<List<ChatMessage>> getSessionMessages(String sessionId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/sessions/$sessionId/messages'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final messages = (data['data'] as List)
            .map((json) => ChatMessage.fromJson(json))
            .toList();
        await LocalStorageService.saveSessionMessages(sessionId, messages);
        return messages;
      }
    } catch (_) {}
    return await LocalStorageService.getSessionMessages(sessionId);
  }

  static Future<ChatMessage> processTextInSession(String sessionId, String text) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/sessions/$sessionId/process'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': text}),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final message = ChatMessage.fromJson(data['data']);
        
        final messages = await LocalStorageService.getSessionMessages(sessionId);
        messages.add(message);
        await LocalStorageService.saveSessionMessages(sessionId, messages);
        return message;
      } else if (response.statusCode == 404) {
        throw Exception('Session not found');
      } else {
        try {
          final error = jsonDecode(response.body);
          throw Exception(error['error'] ?? 'Server error: ${response.statusCode}');
        } catch (_) {
          throw Exception('Server error: ${response.statusCode}');
        }
      }
    } on TimeoutException {
      throw Exception('Request timeout. Please check your connection.');
    } catch (e) {
      if (e.toString().contains('Connection refused')) {
        throw Exception('Cannot connect to server. Make sure backend is running on $baseUrl');
      }
      rethrow;
    }
  }

  static Future<void> deleteSession(String sessionId) async {
    try {
      await http.delete(Uri.parse('$baseUrl/sessions/$sessionId'))
          .timeout(const Duration(seconds: 10));
    } catch (_) {
      // Ignore network errors, still delete locally
    }
    await LocalStorageService.deleteSession(sessionId);
  }

  // Legacy methods
  static Future<ChatMessage> processText(String text) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/process'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': text}),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return ChatMessage.fromJson(data['data']);
      } else {
        throw Exception('Failed to process text: ${response.statusCode}');
      }
    } on TimeoutException {
      throw Exception('Request timeout. Please check your connection.');
    } catch (e) {
      throw Exception('Failed to process text: ${e.toString()}');
    }
  }

  static Future<List<ChatMessage>> getHistory() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/history'))
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return (data['data'] as List)
            .map((json) => ChatMessage.fromJson(json))
            .toList();
      } else {
        throw Exception('Failed to load history: ${response.statusCode}');
      }
    } on TimeoutException {
      throw Exception('Request timeout. Please check your connection.');
    } catch (e) {
      throw Exception('Failed to load history: ${e.toString()}');
    }
  }

  static Future<void> clearHistory() async {
    try {
      final response = await http.post(Uri.parse('$baseUrl/clear-history'))
          .timeout(const Duration(seconds: 10));
      
      if (response.statusCode != 200) {
        throw Exception('Failed to clear history: ${response.statusCode}');
      }
    } on TimeoutException {
      throw Exception('Request timeout. Please check your connection.');
    } catch (e) {
      throw Exception('Failed to clear history: ${e.toString()}');
    }
  }
}
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/chat_session.dart';
import '../models/chat_message.dart';

class LocalStorageService {
  static const String _sessionsKey = 'chat_sessions';
  static const String _messagesPrefix = 'messages_';

  static Future<void> saveSessions(List<ChatSession> sessions) async {
    final prefs = await SharedPreferences.getInstance();
    final sessionsJson = sessions.map((s) => s.toJson()).toList();
    await prefs.setString(_sessionsKey, jsonEncode(sessionsJson));
  }

  static Future<List<ChatSession>> getSessions() async {
    final prefs = await SharedPreferences.getInstance();
    final sessionsString = prefs.getString(_sessionsKey);
    if (sessionsString == null) return [];
    
    final sessionsList = jsonDecode(sessionsString) as List;
    return sessionsList.map((json) => ChatSession.fromJson(json)).toList();
  }

  static Future<void> saveSessionMessages(String sessionId, List<ChatMessage> messages) async {
    final prefs = await SharedPreferences.getInstance();
    final messagesJson = messages.map((m) => m.toJson()).toList();
    await prefs.setString('$_messagesPrefix$sessionId', jsonEncode(messagesJson));
  }

  static Future<List<ChatMessage>> getSessionMessages(String sessionId) async {
    final prefs = await SharedPreferences.getInstance();
    final messagesString = prefs.getString('$_messagesPrefix$sessionId');
    if (messagesString == null) return [];
    
    final messagesList = jsonDecode(messagesString) as List;
    return messagesList.map((json) => ChatMessage.fromJson(json)).toList();
  }

  static Future<void> deleteSession(String sessionId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('$_messagesPrefix$sessionId');
    
    final sessions = await getSessions();
    final updatedSessions = sessions.where((s) => s.id != sessionId).toList();
    await saveSessions(updatedSessions);
  }

  static Future<void> addSession(ChatSession session) async {
    final sessions = await getSessions();
    sessions.add(session);
    await saveSessions(sessions);
  }

  static Future<void> updateSession(ChatSession session) async {
    final sessions = await getSessions();
    final index = sessions.indexWhere((s) => s.id == session.id);
    if (index != -1) {
      sessions[index] = session;
      await saveSessions(sessions);
    }
  }
}
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  const String baseUrl = 'https://pii-security-app.onrender.com/api';
  
  print('Testing backend connection...');
  
  try {
    // Test health endpoint
    print('Testing health endpoint...');
    final healthResponse = await http.get(
      Uri.parse('$baseUrl/health'),
      headers: {'Content-Type': 'application/json'},
    ).timeout(Duration(seconds: 30));
    
    print('Health Status: ${healthResponse.statusCode}');
    if (healthResponse.statusCode == 200) {
      print('Health Response: ${healthResponse.body}');
    }
    
    // Test session creation
    print('\nTesting session creation...');
    final sessionResponse = await http.post(
      Uri.parse('$baseUrl/sessions'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'title': 'Test Session'}),
    ).timeout(Duration(seconds: 30));
    
    print('Session Status: ${sessionResponse.statusCode}');
    if (sessionResponse.statusCode == 201) {
      final sessionData = json.decode(sessionResponse.body);
      print('Session Created: ${sessionData['id']}');
      
      // Test message sending
      print('\nTesting message sending...');
      final messageResponse = await http.post(
        Uri.parse('$baseUrl/sessions/${sessionData['id']}/messages'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'text': 'Hello, test message'}),
      ).timeout(Duration(seconds: 30));
      
      print('Message Status: ${messageResponse.statusCode}');
      if (messageResponse.statusCode == 200) {
        final messageData = json.decode(messageResponse.body);
        print('Message Response: ${messageData['bot_response']}');
      } else {
        print('Message Error: ${messageResponse.body}');
      }
    } else {
      print('Session Error: ${sessionResponse.body}');
    }
    
  } catch (e) {
    print('Error: $e');
  }
}
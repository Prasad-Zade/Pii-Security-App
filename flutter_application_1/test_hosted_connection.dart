import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  print('Testing hosted API connection...');
  
  final url = 'https://pii-security-app.onrender.com/api/sessions';
  
  try {
    print('Connecting to: $url');
    final response = await http.get(Uri.parse(url)).timeout(Duration(seconds: 10));
    print('Status: ${response.statusCode}');
    print('Response: ${response.body}');
    
    if (response.statusCode == 200) {
      print('✅ SUCCESS: Hosted server is working!');
    } else {
      print('❌ Server responded with error: ${response.statusCode}');
    }
  } catch (e) {
    print('❌ Connection failed: $e');
    print('Make sure the server is deployed and running.');
  }
}
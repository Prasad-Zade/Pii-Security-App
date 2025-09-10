import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  print('Testing API connection...');
  
  final urls = [
    'http://localhost:5000/api/sessions',
    'http://10.0.2.2:5000/api/sessions',
    'http://127.0.0.1:5000/api/sessions',
  ];
  
  for (String url in urls) {
    try {
      print('\nTrying: $url');
      final response = await http.get(Uri.parse(url)).timeout(Duration(seconds: 5));
      print('Status: ${response.statusCode}');
      print('Response: ${response.body}');
      if (response.statusCode == 200) {
        print('✅ SUCCESS: $url works!');
        break;
      }
    } catch (e) {
      print('❌ FAILED: $e');
    }
  }
}
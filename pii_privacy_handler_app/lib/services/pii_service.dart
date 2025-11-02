import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart';
import 'pii_dependency_analyzer.dart';

class PIIService {
  static const String baseUrl = 'http://10.216.184.140:5000/api';
  static const List<String> fallbackUrls = [
    'http://10.216.184.140:5000/api',  // Your computer's IP
    'http://10.0.2.2:5000/api',
    'http://127.0.0.1:5000/api',
    'https://pii-backend-deploy.onrender.com/api',
  ];
  
  static Future<ChatMessage> processMessage(String sessionId, String text) async {
    // First analyze PII dependencies locally
    final analysis = PIIDependencyAnalyzer.analyzeQuery(text);
    print('PII Analysis: ${analysis['hasDependentPII'] ? 'Has dependent PII' : 'No dependent PII'}');
    
    try {
      print('[DEBUG] Connecting to backend for session: $sessionId');
      String? workingUrl;
      http.Response? response;
      
      // Try all URLs
      for (final url in fallbackUrls) {
        try {
          print('[DEBUG] Trying: $url');
          response = await http.post(
            Uri.parse('$url/sessions/$sessionId/messages'),
            headers: {'Content-Type': 'application/json'},
            body: json.encode({
              'text': text,
              'pii_analysis': analysis,
            }),
          ).timeout(Duration(seconds: 5));
          
          if (response.statusCode == 200) {
            workingUrl = url;
            print('[SUCCESS] Connected to: $url');
            break;
          }
        } catch (e) {
          print('[ERROR] $url failed: $e');
          continue;
        }
      }
      
      if (response == null || workingUrl == null) {
        throw Exception('All backend URLs failed');
      }

      print('[DEBUG] Backend status: ${response.statusCode}');
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        print('\n' + '='*80);
        print('[FLUTTER] RECEIVED FROM BACKEND');
        final botResp = data['bot_response']?.toString() ?? '';
        final reconResp = data['reconstructed_text']?.toString() ?? '';
        print('  bot_response: ${botResp.substring(0, botResp.length > 80 ? 80 : botResp.length)}...');
        print('  reconstructed_text: ${reconResp.substring(0, reconResp.length > 80 ? 80 : reconResp.length)}...');
        print('  privacy_score: ${data['privacy_score']}');
        
        final message = ChatMessage(
          id: data['id'],
          userMessage: data['user_message'],
          anonymizedText: data['anonymized_text'] ?? analysis['maskedQuery'],
          llmPrompt: data['llm_prompt'] ?? analysis['maskedQuery'],
          botResponse: data['bot_response'],
          reconstructedText: data['reconstructed_text'],
          privacyScore: (data['privacy_score'] as num?)?.toDouble() ?? analysis['privacyScore'],
          processingTime: (data['processing_time'] as num).toDouble(),
          timestamp: DateTime.parse(data['timestamp']),
        );
        
        print('\n[FLUTTER] CREATED MESSAGE OBJECT');
        print('  botResponse: ${message.botResponse.substring(0, message.botResponse.length > 80 ? 80 : message.botResponse.length)}...');
        print('  reconstructedText: ${message.reconstructedText.substring(0, message.reconstructedText.length > 80 ? 80 : message.reconstructedText.length)}...');
        print('  privacyScore: ${message.privacyScore}');
        print('='*80 + '\n');
        
        return message;
      } else {
        throw Exception('HTTP ${response.statusCode}');
      }
    } catch (e) {
      print('Backend failed: $e');
      return await processLocally(text, analysis);
    }
  }
  
  static Future<ChatMessage> processLocally(String text, [Map<String, dynamic>? analysis]) async {
    analysis ??= PIIDependencyAnalyzer.analyzeQuery(text);
    
    final sessionId = 'temp_${DateTime.now().millisecondsSinceEpoch}';
    
    print('[DEBUG] ProcessLocally called for: $text');
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/sessions/$sessionId/messages'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'text': text,
          'pii_analysis': analysis,
        }),
      ).timeout(Duration(seconds: 10));

      print('[DEBUG] ProcessLocally backend status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('[DEBUG] ProcessLocally got bot_response: ${data['bot_response']}');
        
        return ChatMessage(
          id: data['id'],
          userMessage: data['user_message'],
          anonymizedText: data['anonymized_text'] ?? analysis['maskedQuery'],
          llmPrompt: data['llm_prompt'] ?? analysis['maskedQuery'],
          botResponse: data['bot_response'],
          reconstructedText: data['reconstructed_text'],
          privacyScore: (data['privacy_score'] as num?)?.toDouble() ?? analysis['privacyScore'],
          processingTime: (data['processing_time'] as num).toDouble(),
          timestamp: DateTime.parse(data['timestamp']),
        );
      }
    } catch (e) {
      print('[ERROR] ProcessLocally backend failed: $e');
      throw Exception('Backend connection failed. Please ensure the backend server is running.');
    }
    
    throw Exception('Backend connection failed. Please ensure the backend server is running.');
  }
  
  static Future<String> _generateLocalResponse(String originalText, Map<String, dynamic> analysis) async {
    final maskedText = analysis['maskedQuery'] as String;
    final hasDependentPII = analysis['hasDependentPII'] as bool;
    final hasNonDependentPII = analysis['hasNonDependentPII'] as bool;
    
    String contextPrompt = '';
    if (hasDependentPII && hasNonDependentPII) {
      contextPrompt = 'Note: Some personal information has been masked for privacy, but data needed for computation has been preserved. ';
    } else if (hasNonDependentPII) {
      contextPrompt = 'Note: Personal information has been masked for privacy protection. ';
    } else if (hasDependentPII) {
      contextPrompt = 'Note: Data needed for computation has been preserved. ';
    }
    
    return await _callGeminiAPI(contextPrompt + maskedText);
  }
  
  static Future<String> _callGeminiAPI(String text) async {
    print('[ERROR] Local Gemini should not be called - backend should handle this');
    return 'ERROR: Backend connection failed. Local processing disabled.';
  }
  
  static String _getFallbackResponse(String text) {
    return 'Backend connection failed. Please check your connection.';
  }
  
  static String _getResponseForQuery(String text) {
    // Remove hardcoded responses - this should call LLM API
    return 'Please integrate with actual LLM API (Gemini) using your API key to get real responses for: $text';
  }
}
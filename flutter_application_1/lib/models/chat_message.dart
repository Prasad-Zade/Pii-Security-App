class ChatMessage {
  final int id;
  final String? sessionId;
  final String userMessage;
  final String botResponse;
  final String anonymizedText;
  final String reconstructedText;
  final double privacyScore;
  final double processingTime;
  final DateTime timestamp;

  ChatMessage({
    required this.id,
    this.sessionId,
    required this.userMessage,
    required this.botResponse,
    required this.anonymizedText,
    required this.reconstructedText,
    required this.privacyScore,
    required this.processingTime,
    required this.timestamp,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'],
      sessionId: json['session_id'],
      userMessage: json['user_message'],
      botResponse: json['bot_response'],
      anonymizedText: json['anonymized_text'],
      reconstructedText: json['reconstructed_text'],
      privacyScore: json['privacy_score'].toDouble(),
      processingTime: json['processing_time'].toDouble(),
      timestamp: DateTime.parse(json['timestamp']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'session_id': sessionId,
      'user_message': userMessage,
      'bot_response': botResponse,
      'anonymized_text': anonymizedText,
      'reconstructed_text': reconstructedText,
      'privacy_score': privacyScore,
      'processing_time': processingTime,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}
import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../models/chat_session.dart';
import '../services/api_service.dart';
import '../services/local_storage_service.dart';
import '../widgets/message_bubble.dart';
import 'message_details_screen.dart';
import 'history_screen.dart';

class ChatScreen extends StatefulWidget {
  final String? sessionId;
  final VoidCallback? onSessionUpdate;
  
  const ChatScreen({super.key, this.sessionId, this.onSessionUpdate});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  String? _currentSessionId;

  @override
  void initState() {
    super.initState();
    _currentSessionId = widget.sessionId;
    if (_currentSessionId != null) {
      _loadSessionMessages();
    }
  }

  Future<void> _loadSessionMessages() async {
    if (_currentSessionId == null) return;
    
    final messages = await LocalStorageService.getSessionMessages(_currentSessionId!);
    setState(() {
      _messages.clear();
      _messages.addAll(messages);
    });
  }

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _isLoading) return;

    _controller.clear();
    setState(() {
      _isLoading = true;
    });

    try {
      ChatMessage? message;
      
      // Try with existing session first
      if (_currentSessionId != null) {
        try {
          message = await ApiService.processTextInSession(_currentSessionId!, text);
        } catch (e) {
          // Reset session on any error and try creating new one
          _currentSessionId = null;
        }
      }
      
      // Create new session if needed
      if (message == null) {
        final title = text.length > 50 ? text.substring(0, 50) + '...' : text;
        final session = await ApiService.createSession(title: title);
        _currentSessionId = session.id;
        message = await ApiService.processTextInSession(_currentSessionId!, text);
      }
      
      setState(() {
        _messages.add(message!);
        _isLoading = false;
      });
      
      // Update session title if this is the first message
      if (_messages.length == 1 && _currentSessionId != null) {
        final title = text.length > 50 ? text.substring(0, 50) + '...' : text;
        final sessions = await LocalStorageService.getSessions();
        final sessionIndex = sessions.indexWhere((s) => s.id == _currentSessionId);
        if (sessionIndex != -1) {
          final updatedSession = ChatSession(
            id: sessions[sessionIndex].id,
            title: title,
            createdAt: sessions[sessionIndex].createdAt,
            updatedAt: DateTime.now(),
          );
          await LocalStorageService.updateSession(updatedSession);
        }
      }
      
      widget.onSessionUpdate?.call();
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            backgroundColor: const Color(0xFF2F2F2F),
            title: const Row(
              children: [
                Icon(Icons.wifi_off, color: Colors.orange),
                SizedBox(width: 8),
                Text('Connection Issue', style: TextStyle(color: Colors.white)),
              ],
            ),
            content: const Text(
              'Unable to connect to server. Please check your internet connection and try again.',
              style: TextStyle(color: Colors.white),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('OK', style: TextStyle(color: Colors.blue)),
              ),
            ],
          ),
        );
      }
    }
  }

  void _showMessageDetails(ChatMessage message) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => MessageDetailsScreen(message: message),
      ),
    );
  }



  void _showInfoDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.security, color: Colors.blue),
            SizedBox(width: 8),
            Text('How PII Protection Works', style: TextStyle(fontSize: 20),),
          ],
        ),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('📝 Step 1: Your Input'),
            Text('You type your message with personal information.\n'),
            Text('🔒 Step 2: PII Masking'),
            Text('We detect and replace sensitive data with safe placeholders.\n'),
            Text('💡 Step 3: AI Processing'),
            Text('AI processes the masked text (never sees your real data).\n'),
            Text('✅ Step 4: Reconstruction'),
            Text('We restore your original data in the final response.'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Got it!'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFF212121),
      child: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.security,
                          size: 80,
                          color: Colors.grey,
                        ),
                        SizedBox(height: 24),
                        Text(
                          'PII Privacy Protection',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.w600,
                            color: Colors.white,
                          ),
                        ),
                        SizedBox(height: 16),
                        Text(
                          'Your messages are protected through 4 secure steps',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey,
                          ),
                        ),
                        SizedBox(height: 12),
                        Text(
                          '📝 Input → 🔒 Masked → 💡 AI Response → ✅ Reconstructed',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    reverse: true,
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final message = _messages[_messages.length - 1 - index];
                      return MessageBubble(
                        message: message,
                        onTap: () => _showMessageDetails(message),
                      );
                    },
                  ),
          ),
          if (_isLoading)
            Container(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  const LinearProgressIndicator(),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const CircularProgressIndicator(),
                      const SizedBox(width: 16),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Processing your message...',
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          Text(
                            '🔍 Detecting PII → 🔒 Masking → 💡 AI Processing',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: Color(0xFF2F2F2F),
              border: Border(top: BorderSide(color: Color(0xFF404040), width: 1)),
            ),
            child: TextField(
              controller: _controller,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: 'Message PII Privacy Chat...',
                hintStyle: TextStyle(color: Colors.grey[400]),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(25),
                  borderSide: const BorderSide(color: Color(0xFF404040)),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(25),
                  borderSide: const BorderSide(color: Color(0xFF404040)),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(25),
                  borderSide: const BorderSide(color: Colors.blue),
                ),
                filled: true,
                fillColor: const Color(0xFF404040),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.send, color: Colors.white),
                  onPressed: _isLoading ? null : _sendMessage,
                ),
              ),
              maxLines: null,
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
        ],
      ),
    );
  }
}
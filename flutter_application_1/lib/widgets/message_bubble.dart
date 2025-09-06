import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/chat_message.dart';

class MessageBubble extends StatefulWidget {
  final ChatMessage message;
  final VoidCallback? onTap;

  const MessageBubble({
    super.key,
    required this.message,
    this.onTap,
  });

  @override
  State<MessageBubble> createState() => _MessageBubbleState();
}

class _MessageBubbleState extends State<MessageBubble> {
  bool _showProcessSteps = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 1. User Input (Original)
          _buildBubble(
            text: widget.message.userMessage,
            icon: Icons.edit,
            color: const Color(0xFF2F2F2F),
            textColor: Colors.white,
            label: "📝 Your Input",
            alignment: Alignment.centerRight,
          ),
          const SizedBox(height: 8),

          // 2. Final Response (Always visible)
          _buildFinalResponseBubble(),

          // 3. Hidden process steps (toggle with arrow)
          if (_showProcessSteps) ...[
            const SizedBox(height: 6),
            _buildBubble(
              text: widget.message.anonymizedText,
              icon: Icons.lock,
              color: const Color(0xFF4A1A1A),
              textColor: Colors.red[300]!,
              label: "🔒 Masked (PII Protected)",
              alignment: Alignment.centerLeft,
            ),
            const SizedBox(height: 6),
            _buildBubble(
              text: widget.message.botResponse,
              icon: Icons.lightbulb,
              color: const Color(0xFF1A2A4A),
              textColor: Colors.blue[300]!,
              label: "💡 AI Response (Safe)",
              alignment: Alignment.centerLeft,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildBubble({
    required String text,
    required IconData icon,
    required Color color,
    required Color textColor,
    required String label,
    required Alignment alignment,
  }) {
    return Align(
      alignment: alignment,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.85,
        ),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFF404040)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(icon, size: 16, color: textColor),
                const SizedBox(width: 6),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: textColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              text.isEmpty ? 'No content available' : text,
              style: TextStyle(color: textColor),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFinalResponseBubble() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.85,
        ),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: const Color(0xFF1A4A2A),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFF2A6A3A)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.check_circle, size: 16, color: Colors.green[300]),
                const SizedBox(width: 6),
                Text(
                  "✅ Final Result",
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: Colors.green[300],
                  ),
                ),
                const Spacer(),
                InkWell(
                  onTap: () {
                    setState(() {
                      _showProcessSteps = !_showProcessSteps;
                    });
                  },
                  child: Icon(
                    _showProcessSteps
                        ? Icons.keyboard_arrow_up
                        : Icons.keyboard_arrow_down,
                    color: Colors.green[300],
                    size: 20,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              widget.message.reconstructedText.isEmpty
                  ? widget.message.botResponse
                  : widget.message.reconstructedText,
              style: TextStyle(color: Colors.green[300]),
            ),
            const SizedBox(height: 4),
            Text(
              DateFormat('MMM dd, HH:mm').format(widget.message.timestamp),
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

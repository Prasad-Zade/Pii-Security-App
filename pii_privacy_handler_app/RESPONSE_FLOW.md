# Response Flow - No Hardcoded Messages

## Backend Response Structure

The backend (`pii_dependency_handler.py`) generates responses using **Gemini API** and returns:

```json
{
  "llm_response": "Raw LLM response with masked PII",
  "llm_response_reconstructed": "LLM response with original PII restored",
  "bot_response": "Same as llm_response (for compatibility)",
  "reconstructed_text": "Same as llm_response_reconstructed"
}
```

## Flutter App Flow

### 1. User sends message
- `chat_screen.dart` → `PIIService.processMessage()`

### 2. Backend Processing
- `pii_service.dart` sends request to backend
- Backend calls Gemini API with masked query
- Backend reconstructs response with original PII
- Returns `llm_response_reconstructed`

### 3. Display Response
- `message_bubble.dart` displays: `reconstructedText` (priority) or `botResponse` (fallback)
- This ensures the **real LLM response** is always shown

## Key Files Updated

1. **lib/services/pii_service.dart**
   - Uses `llm_response_reconstructed` from backend
   - Removed hardcoded fallback responses
   - Throws error if backend unavailable

2. **lib/widgets/message_bubble.dart**
   - Displays `reconstructedText` (contains real LLM response)
   - Falls back to `botResponse` only if reconstructedText is empty

3. **backend/pii_dependency_handler.py**
   - Calls Gemini API: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`
   - Returns real LLM responses in `llm_response_reconstructed`

## Testing

Run backend:
```bash
cd backend
python start_with_llm.py
```

Run Flutter app:
```bash
flutter run -d windows
```

Send a message and verify:
- Response is from Gemini API (not hardcoded)
- PII is properly reconstructed in the response
- No fallback messages appear when backend is running

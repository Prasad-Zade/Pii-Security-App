# Optimized Backend-Frontend Connection

## ✅ Current Setup (Already Optimized)

### Backend: `pii_dependency_handler.py`
**Location:** `backend/pii_dependency_handler.py`

**Features:**
- ✅ Dependent/Non-dependent PII detection
- ✅ Gemini API integration (gemini-2.5-flash)
- ✅ PII reconstruction in responses
- ✅ Context-aware processing
- ✅ Faker-based masking

**API Key:** `AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo`

### Frontend: `pii_service.dart`
**Location:** `lib/services/pii_service.dart`

**Connection:**
- ✅ Sends PII analysis to backend
- ✅ Receives `llm_response_reconstructed` (real Gemini response)
- ✅ Displays reconstructed text with original PII

## Data Flow

```
User Input
    ↓
Frontend PII Analysis (pii_dependency_analyzer.dart)
    ↓
Send to Backend (pii_service.dart)
    ↓
Backend Processing (pii_dependency_handler.py)
    ├─ Detect PII entities
    ├─ Mask non-dependent PII with Faker
    ├─ Keep dependent PII (for calculations)
    ├─ Call Gemini API
    └─ Reconstruct response with original PII
    ↓
Return to Frontend
    ↓
Display reconstructed_text (message_bubble.dart)
```

## Backend Response Structure

```json
{
  "llm_response": "Raw Gemini response with fake PII",
  "llm_response_reconstructed": "Gemini response with original PII restored",
  "final_response": "Same as llm_response_reconstructed",
  "masked_query": "Query sent to Gemini with fake PII",
  "detected_entities": ["name", "phone"],
  "entities_masked": ["name"],
  "entities_preserved": ["phone"]
}
```

## Running the Optimized Setup

### Terminal 1 - Backend
```bash
cd d:\BE\AmazonQ\Pii-Security-App\pii_privacy_handler_app\backend
python start_with_llm.py
```

### Terminal 2 - Flutter
```bash
cd d:\BE\AmazonQ\Pii-Security-App\pii_privacy_handler_app
flutter run -d windows
```

## Test Cases

### Test 1: Name Introduction (Non-dependent PII)
**Input:** `Hi, my name is Prasad`
**Expected:**
- Name masked with Faker in backend
- Gemini generates response
- Response displayed without exposing real name

### Test 2: Phone Calculation (Dependent PII)
**Input:** `My phone is 9876543210, add all digits`
**Expected:**
- Phone kept for calculation
- Gemini calculates: 9+8+7+6+5+4+3+2+1+0 = 45
- Response includes original phone number

### Test 3: Mixed PII
**Input:** `I am John, my phone is 1234567890, calculate digit sum`
**Expected:**
- Name masked (non-dependent)
- Phone preserved (dependent)
- Calculation performed correctly

## Verification

Check backend logs for:
```
[DEBUG] Calling Gemini for: ...
[DEBUG] Full response: ...
```

Check frontend logs for:
```
[SUCCESS] Connected to: http://127.0.0.1:5000/api
[DEBUG] Bot response: ...
[DEBUG] Returning message with bot response: ...
```

## Status Check

Backend health: `http://127.0.0.1:5000/api/health`

Expected response:
```json
{
  "status": "healthy",
  "privacy_handler_available": true,
  "model_type": "PIIDependencyHandler"
}
```

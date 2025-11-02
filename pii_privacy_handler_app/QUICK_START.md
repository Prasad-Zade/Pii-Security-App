# Quick Start Guide - Optimized Setup

## ✅ Your Setup is Already Optimized!

The backend is using **`pii_dependency_handler.py`** - the most optimized model with:
- Gemini API integration
- Dependent/Non-dependent PII detection
- PII reconstruction
- Context-aware processing

## Step 1: Start Backend

Open **Terminal 1**:
```bash
cd d:\BE\AmazonQ\Pii-Security-App\pii_privacy_handler_app\backend
python start_with_llm.py
```

**Expected output:**
```
==================================================
PII Privacy Handler Backend with Gemini LLM
==================================================
[OK] Gemini API configured - Real LLM responses enabled

Starting server on http://127.0.0.1:5000
```

## Step 2: Test Backend (Optional)

Open **Terminal 2**:
```bash
cd d:\BE\AmazonQ\Pii-Security-App\pii_privacy_handler_app\backend
python test_optimized_connection.py
```

**Expected:** All tests pass ✅

## Step 3: Start Flutter App

Open **Terminal 3** (or Terminal 2 if you skipped testing):
```bash
cd d:\BE\AmazonQ\Pii-Security-App\pii_privacy_handler_app
flutter run -d windows
```

## Step 4: Test in App

### Test 1: Simple Introduction
**Type:** `Hi, my name is Prasad`

**Expected:**
- Name is masked in backend
- Gemini generates natural response
- No hardcoded message

### Test 2: Phone Calculation
**Type:** `My phone is 9876543210, add all digits`

**Expected:**
- Phone number preserved for calculation
- Gemini calculates: 45
- Response includes calculation result

### Test 3: General Question
**Type:** `What is artificial intelligence?`

**Expected:**
- Real Gemini response about AI
- No PII detected
- Natural conversation

## Verification Checklist

✅ Backend shows: `[DEBUG] Calling Gemini for: ...`
✅ Backend shows: `[DEBUG] Full response: ...`
✅ Flutter shows: `[SUCCESS] Connected to: http://127.0.0.1:5000/api`
✅ Responses are from Gemini (not hardcoded)
✅ PII is properly masked/preserved based on context

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Install requirements: `pip install -r requirements.txt`

### Flutter can't connect
- Verify backend is running on port 5000
- Check firewall settings
- Try: `http://127.0.0.1:5000/api/health` in browser

### No Gemini responses
- Check API key in `pii_dependency_handler.py`
- Verify internet connection
- Check Gemini API quota

## Architecture

```
Flutter App (Frontend)
    ↓
pii_service.dart
    ↓
HTTP POST to Backend
    ↓
app.py (Flask)
    ↓
pii_dependency_handler.py (Optimized Model)
    ↓
Gemini API (gemini-2.5-flash)
    ↓
Response with PII Reconstruction
    ↓
Display in message_bubble.dart
```

## Success Indicators

1. **Backend logs show Gemini API calls**
2. **Responses are contextual and intelligent**
3. **PII is masked appropriately**
4. **Calculations work with preserved PII**
5. **No hardcoded fallback messages**

---

**You're all set! The optimized backend is already connected to your frontend.** 🎉

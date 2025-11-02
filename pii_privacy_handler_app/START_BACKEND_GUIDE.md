# Backend Startup Guide

## Quick Start (Recommended)

### Step 1: Start the Backend Server

Open a terminal in the `backend` folder and run:

```bash
cd backend
python app.py
```

You should see:
```
[SUCCESS] Comprehensive PII Handler ready!
[STARTUP] Starting PII Privacy Handler Backend...
[INFO] Server starting on port 5000
 * Running on http://0.0.0.0:5000
```

### Step 2: Test the Backend

Open another terminal and run:

```bash
cd backend
python test_simple.py
```

Expected output:
```
✅ Backend is running!
✅ Session created
✅ Message processed successfully!
```

### Step 3: Run Your Flutter App

Now your Flutter app should connect successfully!

---

## Troubleshooting

### Issue: "Cannot connect to backend"

**Solution 1: Check if backend is running**
```bash
python test_simple.py
```

**Solution 2: Install missing packages**
```bash
pip install flask flask-cors requests faker google-generativeai
```

**Solution 3: Use the quick start script**
```bash
quick_start.bat
```

### Issue: "Module not found" errors

Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Flutter app shows "Connection refused"

1. Make sure backend is running (you should see "Running on http://0.0.0.0:5000")
2. Check if port 5000 is not blocked by firewall
3. For Android emulator, the app tries these URLs in order:
   - http://10.0.2.2:5000 (Android emulator)
   - http://127.0.0.1:5000 (localhost)
   - https://pii-backend-deploy.onrender.com (cloud backup)

---

## Testing the PII Analyzer

Run the Dart tests:

```bash
# Test the PII dependency analyzer
dart test_pii.dart

# Run comprehensive tests
dart comprehensive_test.dart
```

Expected: 9/10 tests passing (90% success rate)

---

## What the Backend Does

1. **Detects PII**: Names, phones, emails, addresses
2. **Analyzes Dependencies**: Determines if PII is needed for computation
3. **Masks Non-Dependent PII**: Replaces with fake data
4. **Preserves Dependent PII**: Keeps data needed for calculations
5. **Processes with LLM**: Sends masked query to Gemini API
6. **Reconstructs Response**: Replaces fake data with original PII

---

## Backend Endpoints

- `GET /api/health` - Check if backend is running
- `POST /api/sessions` - Create a new chat session
- `POST /api/sessions/{id}/messages` - Send a message
- `GET /api/sessions/{id}/messages` - Get message history
- `DELETE /api/sessions/{id}` - Delete a session

---

## Next Steps

1. ✅ Start backend: `python app.py`
2. ✅ Test connection: `python test_simple.py`
3. ✅ Run Flutter app
4. ✅ Test with PII messages:
   - "My name is John and my phone is 1234567890"
   - "Calculate the sum of digits in 9876543210"
   - "My email is test@example.com"

---

## Support

If you still have issues:
1. Check that Python 3.8+ is installed: `python --version`
2. Verify all packages are installed: `pip list`
3. Check backend logs for errors
4. Ensure port 5000 is not in use by another application

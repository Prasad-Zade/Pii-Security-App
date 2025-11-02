# PII Privacy Handler App

A Flutter application integrated with the AmazonQ Model V1 backend for advanced PII (Personally Identifiable Information) detection and privacy protection.

## Architecture

```
┌─────────────────────┐    HTTP API    ┌──────────────────────┐
│   Flutter App       │ ◄─────────────► │   Flask Backend      │
│   (Frontend)        │                 │   (Python)           │
└─────────────────────┘                 └──────────────────────┘
                                                    │
                                                    ▼
                                        ┌──────────────────────┐
                                        │  AmazonQ Model V1    │
                                        │  PII Privacy Handler │
                                        └──────────────────────┘
```

## Features

### Frontend (Flutter)
- **Chat Interface**: Clean, modern chat UI with message bubbles
- **Session Management**: Create, rename, and delete chat sessions
- **Privacy Scoring**: Real-time privacy score display for each message
- **Offline Support**: Fallback to local processing when backend is unavailable
- **Connection Status**: Visual indicator showing backend connection status
- **Message History**: Persistent storage of chat sessions and messages

### Backend (Flask + AmazonQ Model V1)
- **Advanced PII Detection**: Uses the sophisticated PII detection from AmazonQ Model V1
- **Context-Aware Processing**: Intelligent masking based on query context
- **Gemini AI Integration**: Optional integration with Google's Gemini API
- **Realistic Data Replacement**: Uses Faker library for generating realistic fake data
- **RESTful API**: Clean API endpoints for all operations

## Setup Instructions

### Prerequisites
- **Flutter SDK** (3.7.2 or higher)
- **Python** (3.8 or higher)
- **Git**

### 1. Clone and Setup Flutter App

```bash
cd d:\BE\AmazonQ\pii_privacy_handler_app
flutter pub get
```

### 2. Setup Backend

#### Windows:
```bash
cd backend
start_backend.bat
```

#### Linux/macOS:
```bash
cd backend
chmod +x start_backend.sh
./start_backend.sh
```

#### Manual Setup:
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

### 3. Run Flutter App

```bash
flutter run
```

## API Endpoints

### Backend API (http://localhost:5000/api)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check backend health and PII handler status |
| POST | `/sessions` | Create a new chat session |
| GET | `/sessions` | Get all chat sessions |
| DELETE | `/sessions/{id}` | Delete a specific session |
| POST | `/sessions/{id}/messages` | Process a message in a session |
| GET | `/sessions/{id}/messages` | Get all messages in a session |
| POST | `/clear-history` | Clear all sessions and messages |

### Example API Usage

#### Create Session
```bash
curl -X POST http://localhost:5000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat"}'
```

#### Process Message
```bash
curl -X POST http://localhost:5000/api/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"text": "Hi, my name is John and my email is john@example.com"}'
```

## Configuration

### Environment Variables (Backend)
Create a `.env` file in the AmazonQ model directory:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### Flutter Configuration
The app automatically detects backend availability and falls back to local mode if needed.

## PII Detection Capabilities

The integrated system can detect and handle:

### Direct PII
- **Names**: Full names, first names with context
- **Email Addresses**: All standard email formats
- **Phone Numbers**: Various phone number formats
- **Aadhaar Numbers**: Indian national ID numbers
- **Account Numbers**: Bank account numbers
- **Credit Card Numbers**: All major card formats
- **SSN**: Social Security Numbers
- **Medical IDs**: Patient IDs, medical record numbers

### Indirect PII
- **Age**: Age mentions in context
- **Location**: Cities, addresses
- **Job Information**: Job titles, employers
- **Education**: Fields of study, institutions

### Context-Aware Processing
- **Mathematical Queries**: Preserves numbers needed for calculations
- **Medical Context**: Handles medical information appropriately
- **Financial Context**: Manages financial data with care
- **General Queries**: Applies standard privacy protection

## Usage Examples

### Example 1: Basic PII Detection
**Input**: "Hi, my name is John Smith and my email is john.smith@company.com"
**Output**: 
- Detected: NAME, EMAIL
- Masked: "Hi, my name is Michael Johnson and my email is sarah.wilson@example.org"
- Privacy Score: 85%

### Example 2: Mathematical Context
**Input**: "My phone number is 1234567890. Can you add all the digits?"
**Output**:
- Detected: PHONE
- Preserved: Phone number (needed for calculation)
- Response: "The sum of all digits in the phone number 1234567890 is: 45"
- Privacy Score: 75%

### Example 3: Medical Context
**Input**: "Patient John Doe, ID P-12345, needs prescription refill"
**Output**:
- Detected: NAME, PATIENT_ID
- Context: Medical
- Appropriate handling based on medical context

## Troubleshooting

### Backend Issues
1. **Import Error**: Ensure the AmazonQ model path is correct
2. **Port Conflict**: Change port in `app.py` if 5000 is occupied
3. **Dependencies**: Run `pip install -r requirements.txt`

### Flutter Issues
1. **HTTP Error**: Check if backend is running on localhost:5000
2. **Dependencies**: Run `flutter pub get`
3. **Build Issues**: Run `flutter clean` then `flutter pub get`

### Connection Issues
- The app shows connection status in the top bar
- Green dot = Backend connected
- Orange dot = Local mode (offline)

## Development

### Adding New PII Types
1. Update patterns in `privacy_handler.py`
2. Add corresponding fake data generation
3. Test with various input formats

### Extending API
1. Add new endpoints in `app.py`
2. Update Flutter `ApiService` class
3. Handle new response formats in UI

## Security Notes

- All PII detection happens locally or on your controlled backend
- No data is sent to external services without explicit configuration
- Gemini API integration is optional and can be disabled
- Local fallback ensures functionality without internet

## License

This project integrates with the AmazonQ Model V1. Please refer to the original project's license terms.

## Support

For issues related to:
- **Flutter App**: Check Flutter and Dart documentation
- **Backend Integration**: Review Flask and Python setup
- **PII Detection**: Refer to AmazonQ Model V1 documentation
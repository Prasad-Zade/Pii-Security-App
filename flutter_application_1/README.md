# PII Privacy Protection Flutter App

A ChatGPT-like mobile application that connects to the PII Privacy Protection backend system.

## Features

- **ChatGPT-like Interface**: Clean, modern chat interface
- **Real-time PII Processing**: Automatically detects and anonymizes PII in messages
- **Privacy Scores**: Shows privacy protection scores for each message
- **Secure Chat History**: View and manage previous conversations
- **Message Details**: Detailed view of anonymization process
- **Cross-platform**: Works on Android, iOS, and other Flutter-supported platforms

## Setup Instructions

### 1. Backend Setup
First, ensure the backend is running:

```bash
cd "d:\BE Project Claude"
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python api_server.py
```

Or use the provided batch file:
```bash
start_backend.bat
```

The backend will run on `http://localhost:5000`

### 2. Flutter App Setup

```bash
cd flutter_application_1
flutter pub get
flutter run
```

### 3. For Real Device Testing

#### Android:
1. Enable Developer Options and USB Debugging on your device
2. Connect via USB
3. Run: `flutter run`

#### iOS:
1. Open `ios/Runner.xcworkspace` in Xcode
2. Configure signing and provisioning
3. Run from Xcode or use `flutter run`

## API Configuration

The app connects to the backend at `http://localhost:5000/api`. 

For real device testing, update the `baseUrl` in `lib/services/api_service.dart`:

```dart
// For real devices, use your computer's IP address
static const String baseUrl = 'http://YOUR_COMPUTER_IP:5000/api';
```

Find your IP with:
- Windows: `ipconfig`
- Mac/Linux: `ifconfig`

## App Structure

```
lib/
├── models/
│   └── chat_message.dart      # Data model for chat messages
├── services/
│   └── api_service.dart       # Backend API communication
├── screens/
│   ├── chat_screen.dart       # Main chat interface
│   ├── history_screen.dart    # Chat history management
│   └── message_details_screen.dart  # Detailed message view
├── widgets/
│   └── message_bubble.dart    # Chat message UI component
└── main.dart                  # App entry point
```

## Privacy Features

- **PII Detection**: Automatically identifies personal information
- **Anonymization**: Replaces PII with safe alternatives
- **Privacy Scoring**: Rates the privacy protection level (0-100%)
- **Secure Storage**: Chat history stored securely
- **Data Reconstruction**: Shows how original data can be restored

## Usage

1. **Start Conversation**: Type a message containing personal information
2. **View Processing**: See anonymized text and AI response
3. **Check Privacy Score**: Monitor protection level for each message
4. **Access History**: View all previous conversations
5. **Message Details**: Tap any message for detailed processing information
6. **Clear History**: Securely remove all chat data when needed
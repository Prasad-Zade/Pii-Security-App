import 'dart:io';

class NetworkService {
  static String getBaseUrl() {
    // Use local server for development
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:5000/api';
    } else if (Platform.isIOS) {
      return 'http://localhost:5000/api';
    } else {
      return 'http://localhost:5000/api';
    }
    
    // Hosted server URL (uncomment to use)
    // return 'https://pii-security-app.onrender.com/api';
  }
}
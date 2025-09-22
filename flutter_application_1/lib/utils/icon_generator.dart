import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class IconGenerator {
  static Future<Uint8List?> loadPrivacyIconFromAssets(String path) async {
    try {
      final byteData = await rootBundle.load(path);
      return byteData.buffer.asUint8List();
    } catch (e) {
      // Return null if asset not found
      return null;
    }
  }
}

// Usage in a widget
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Uint8List?>(
      future: IconGenerator.loadPrivacyIconFromAssets("assets/icon/icon.png"),
      builder: (context, snapshot) {
        if (snapshot.hasData && snapshot.data != null) {
          return Image.memory(
            snapshot.data!,
            width: 128,
            height: 128,
            fit: BoxFit.contain,
          );
        } else if (snapshot.hasError || (snapshot.connectionState == ConnectionState.done && snapshot.data == null)) {
          // Fallback to default icon if asset not found
          return const Icon(
            Icons.security,
            size: 128,
            color: Colors.blue,
          );
        } else {
          return const CircularProgressIndicator();
        }
      },
    );
  }
}

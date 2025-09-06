import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class IconGenerator {
  static Future<Uint8List> loadPrivacyIconFromAssets(String path) async {
    final byteData = await rootBundle.load(path);
    return byteData.buffer.asUint8List();
  }
}

// Usage in a widget
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Uint8List>(
      future: IconGenerator.loadPrivacyIconFromAssets("assets/icon/icon.png"),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Image.memory(
            snapshot.data!,
            width: 128,   // increase width
            height: 128,  // increase height
            fit: BoxFit.contain,
          );
        } else {
          return const CircularProgressIndicator();
        }
      },
    );
  }
}

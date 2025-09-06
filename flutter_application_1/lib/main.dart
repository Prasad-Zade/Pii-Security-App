import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  runApp(const PIIPrivacyApp());
}

class PIIPrivacyApp extends StatelessWidget {
  const PIIPrivacyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PII Privacy Chat',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF212121),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2F2F2F),
          elevation: 0,
        ),
        cardColor: const Color(0xFF2F2F2F),
        dividerColor: const Color(0xFF404040),
      ),
      home: const SplashScreen(),
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(context).copyWith(textScaleFactor: 1.0),
          child: child!,
        );
      },
      debugShowCheckedModeBanner: false,
    );
  }
}

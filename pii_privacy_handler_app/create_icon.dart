import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Create icon with shield and lock
  final recorder = ui.PictureRecorder();
  final canvas = Canvas(recorder);
  final size = 512.0;
  
  // Background
  final bgPaint = Paint()..color = Color(0xFF2F2F2F);
  canvas.drawRect(Rect.fromLTWH(0, 0, size, size), bgPaint);
  
  // Shield
  final shieldPath = Path();
  shieldPath.moveTo(size * 0.5, size * 0.15);
  shieldPath.lineTo(size * 0.75, size * 0.25);
  shieldPath.lineTo(size * 0.75, size * 0.55);
  shieldPath.quadraticBezierTo(size * 0.75, size * 0.75, size * 0.5, size * 0.85);
  shieldPath.quadraticBezierTo(size * 0.25, size * 0.75, size * 0.25, size * 0.55);
  shieldPath.lineTo(size * 0.25, size * 0.25);
  shieldPath.close();
  
  final shieldPaint = Paint()
    ..color = Color(0xFF4CAF50)
    ..style = PaintingStyle.fill;
  canvas.drawPath(shieldPath, shieldPaint);
  
  // Lock
  final lockRect = Rect.fromLTWH(size * 0.42, size * 0.5, size * 0.16, size * 0.2);
  final lockPaint = Paint()
    ..color = Colors.white
    ..style = PaintingStyle.fill;
  canvas.drawRRect(RRect.fromRectAndRadius(lockRect, Radius.circular(8)), lockPaint);
  
  // Lock arc
  final arcRect = Rect.fromLTWH(size * 0.44, size * 0.38, size * 0.12, size * 0.15);
  final arcPaint = Paint()
    ..color = Colors.white
    ..style = PaintingStyle.stroke
    ..strokeWidth = 8;
  canvas.drawArc(arcRect, 3.14, 3.14, false, arcPaint);
  
  final picture = recorder.endRecording();
  final img = await picture.toImage(size.toInt(), size.toInt());
  final byteData = await img.toByteData(format: ui.ImageByteFormat.png);
  final buffer = byteData!.buffer.asUint8List();
  
  await File('assets/icon.png').writeAsBytes(buffer);
  await File('assets/icon_foreground.png').writeAsBytes(buffer);
  
  print('Icon created successfully!');
}

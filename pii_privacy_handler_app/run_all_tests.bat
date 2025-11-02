@echo off
echo ========================================
echo Running All Tests
echo ========================================
echo.

echo [1/2] Testing PII Dependency Analyzer (Dart)
echo ----------------------------------------
dart comprehensive_test.dart
echo.

echo.
echo [2/2] Testing Backend Connection (Python)
echo ----------------------------------------
cd backend
python test_simple.py
cd ..

echo.
echo ========================================
echo Tests Complete!
echo ========================================
pause

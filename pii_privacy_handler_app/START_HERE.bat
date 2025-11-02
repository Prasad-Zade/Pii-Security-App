@echo off
color 0A
echo.
echo ========================================
echo   PII Privacy Handler - Quick Start
echo ========================================
echo.
echo This will:
echo  1. Test the PII Analyzer
echo  2. Start the Backend Server
echo.
echo Press any key to continue...
pause >nul

cls
echo ========================================
echo Step 1: Testing PII Analyzer
echo ========================================
echo.
dart comprehensive_test.dart

echo.
echo ========================================
echo Step 2: Starting Backend Server
echo ========================================
echo.
echo Backend will start on http://localhost:5000
echo.
echo IMPORTANT: Keep this window open!
echo Press Ctrl+C to stop the server
echo.
echo Now you can run your Flutter app!
echo ========================================
echo.

cd backend
python app.py

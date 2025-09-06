@echo off
echo Starting PII Privacy Server...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python api_server.py
pause
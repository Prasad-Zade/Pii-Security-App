@echo off
echo Starting PII Privacy Protection Backend...
echo.
echo Make sure you have installed dependencies:
echo pip install -r requirements.txt
echo python -m spacy download en_core_web_sm
echo.
echo Starting Flask API server on http://localhost:5000
echo.
python api_server.py
pause
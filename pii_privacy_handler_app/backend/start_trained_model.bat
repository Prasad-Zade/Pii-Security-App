@echo off
echo 🔒 Starting PII Privacy Handler with Trained Model
echo ================================================

cd /d "%~dp0"

echo 📦 Installing requirements...
pip install -r requirements.txt

echo 🚀 Starting server with trained model...
python start_with_trained_model.py

pause
PII Privacy Protection System v2
- Modern Tkinter UI using ttkbootstrap
- CSV import/export
- Improved detection & anonymization
- Gemini connector (mock if no API key)

Run:
  python -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  python -m spacy download en_core_web_sm
  python run_gui.py

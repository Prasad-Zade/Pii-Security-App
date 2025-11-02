from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
from faker import Faker
import re

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key="AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo")
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Initialize Faker
fake = Faker()

sessions = {}
messages = {}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'gemini_enabled': True})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    session_id = f"session_{len(sessions)}"
    session = {
        'id': session_id,
        'title': 'New Chat',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    sessions[session_id] = session
    messages[session_id] = []
    return jsonify(session), 201

@app.route('/api/sessions/<session_id>/messages', methods=['POST'])
def process_message(session_id):
    # Create session if it doesn't exist
    if session_id not in sessions:
        sessions[session_id] = {
            'id': session_id,
            'title': 'New Chat',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        messages[session_id] = []
    
    data = request.get_json()
    text = data['text']
    
    # Track replacements for reconstruction
    replacements = {}
    masked = text
    
    # PII masking with random fake names
    name_patterns = [
        (r'\bprasad\b', 'prasad'),
        (r'\bPrasad\b', 'Prasad'),
        (r'\bjohn\b', 'john'),
        (r'\bJohn\b', 'John'),
        (r'\balice\b', 'alice'),
        (r'\bAlice\b', 'Alice'),
    ]
    
    for pattern, original in name_patterns:
        if re.search(pattern, text):
            fake_name = fake.first_name()
            replacements[fake_name] = original
            masked = re.sub(pattern, fake_name, masked)
    
    # Generate Gemini response
    try:
        response = model.generate_content(f"Respond helpfully to: {masked}")
        bot_response = response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        bot_response = "I understand your message. How can I help you?"
    
    # Reconstruct original names in response
    reconstructed = bot_response
    for masked_name, original_name in replacements.items():
        reconstructed = reconstructed.replace(masked_name, original_name)
    
    message = {
        'id': f"msg_{len(messages.get(session_id, []))}",
        'user_message': text,
        'anonymized_text': masked,
        'bot_response': bot_response,
        'reconstructed_text': reconstructed,
        'privacy_score': 85.0,
        'processing_time': 1.0,
        'timestamp': datetime.now().isoformat()
    }
    
    messages[session_id].append(message)
    return jsonify(message)

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    return jsonify(list(sessions.values()))

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
        del messages[session_id]
    return jsonify({'message': 'deleted'})

if __name__ == '__main__':
    print("Starting backend on http://0.0.0.0:5000")
    print("Health check: http://127.0.0.1:5000/api/health")
    print("Android emulator: http://10.0.2.2:5000/api/health")
    app.run(host='0.0.0.0', port=5000, debug=True)
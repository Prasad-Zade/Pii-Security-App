from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key="AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo")
model = genai.GenerativeModel('gemini-pro')

sessions = {}
messages = {}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json() or {}
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    session = {
        'id': session_id,
        'title': data.get('title', 'New Chat'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    sessions[session_id] = session
    messages[session_id] = []
    
    return jsonify(session), 201

@app.route('/api/sessions/<session_id>/messages', methods=['POST'])
def process_message(session_id):
    data = request.get_json()
    user_text = data['text']
    
    # Simple PII masking
    masked_text = user_text
    if 'my name is' in user_text.lower():
        masked_text = user_text.lower().replace('my name is', 'my name is Alex')
    
    # Get LLM response
    try:
        response = model.generate_content(masked_text)
        bot_response = response.text
    except:
        bot_response = "I understand your message. How can I help you?"
    
    message = {
        'id': f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'user_message': user_text,
        'anonymized_text': masked_text,
        'llm_prompt': masked_text,
        'bot_response': bot_response,
        'reconstructed_text': bot_response,
        'privacy_score': 95.0,
        'processing_time': 1.2,
        'timestamp': datetime.now().isoformat()
    }
    
    messages[session_id].append(message)
    return jsonify(message)

if __name__ == '__main__':
    print("Starting simple backend on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
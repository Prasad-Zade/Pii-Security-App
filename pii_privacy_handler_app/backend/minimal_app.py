from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from model_wrapper import get_model_wrapper

app = Flask(__name__)
CORS(app)

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
    print(f"Processing message for session: {session_id}")
    data = request.get_json()
    user_text = data['text']
    print(f"User text: {user_text}")
    
    # Use model wrapper for PII processing
    model_wrapper = get_model_wrapper()
    result = model_wrapper.process_query(user_text)
    
    print(f"Original: {user_text}")
    print(f"Masked: {result['masked_query']}")
    print(f"LLM Response: {result['llm_response']}")
    print(f"Final Response: {result['final_response']}")
    
    message = {
        'id': f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'user_message': user_text,
        'anonymized_text': result['masked_query'],
        'llm_prompt': result['masked_query'],
        'bot_response': result['llm_response'],
        'reconstructed_text': result['final_response'],
        'privacy_score': 95.0,
        'processing_time': 1.2,
        'timestamp': datetime.now().isoformat()
    }
    
    if session_id not in messages:
        messages[session_id] = []
    messages[session_id].append(message)
    
    return jsonify(message)

if __name__ == '__main__':
    print("Starting backend with model wrapper on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
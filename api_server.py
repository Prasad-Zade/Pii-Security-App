from flask import Flask, request, jsonify
from flask_cors import CORS
from src.core.pii_system import PIIPrivacySystem
import json
from datetime import datetime
import os
import uuid

app = Flask(__name__)
CORS(app)

# Initialize PII system
try:
    pii_system = PIIPrivacySystem()
except Exception as e:
    print(f"Warning: PII system initialization failed: {e}")
    pii_system = None

# Stateless server - no storage

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    return jsonify({'success': True, 'data': []})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    title = data.get('title', 'New Chat')
    session_id = str(uuid.uuid4())
    now = datetime.now()
    
    return jsonify({
        'success': True,
        'data': {
            'id': session_id,
            'title': title,
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
    })

@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    return jsonify({'success': True, 'data': []})

@app.route('/api/sessions/<session_id>/process', methods=['POST'])
def process_text_in_session(session_id):
    try:
            
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Process the text
        result = pii_system.process(text, include_llm=True)
        
        # Return processed result without storing
        chat_entry = {
            'id': 1,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'user_message': result.original_text,
            'bot_response': result.llm_response,
            'anonymized_text': result.anonymized_text,
            'reconstructed_text': result.reconstructed_text,
            'privacy_score': result.privacy_score,
            'processing_time': result.processing_time
        }
        
        return jsonify({
            'success': True,
            'data': chat_entry
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Process the text
        result = pii_system.process(text, include_llm=True)
        
        # Return processed result without storing
        chat_entry = {
            'id': 1,
            'timestamp': datetime.now().isoformat(),
            'user_message': result.original_text,
            'bot_response': result.llm_response,
            'anonymized_text': result.anonymized_text,
            'reconstructed_text': result.reconstructed_text,
            'privacy_score': result.privacy_score,
            'processing_time': result.processing_time
        }
        
        return jsonify({
            'success': True,
            'data': chat_entry
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    return jsonify({'success': True, 'message': 'Session deleted'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
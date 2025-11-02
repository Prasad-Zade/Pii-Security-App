from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from model_wrapper import get_model_wrapper
from pii_dependency_handler import PIIDependencyHandler

app = Flask(__name__)
CORS(app)

model_wrapper = get_model_wrapper()
pii_handler = PIIDependencyHandler()
sessions = {}
messages = {}

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'PII Security App Backend is running!'})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'privacy_handler_available': True,
        'amazonq_model_active': True,
        'model_type': 'Deployment',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json() or {}
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(sessions)}"
        
        session = {
            'id': session_id,
            'title': data.get('title', 'New Chat'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        sessions[session_id] = session
        messages[session_id] = []
        
        return jsonify(session), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    try:
        return jsonify(list(sessions.values()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>/messages', methods=['GET', 'POST'])
def handle_messages(session_id):
    try:
        if session_id not in sessions:
            sessions[session_id] = {
                'id': session_id,
                'title': 'Auto-created Chat',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            messages[session_id] = []
        
        if request.method == 'GET':
            return jsonify(messages.get(session_id, []))
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        user_text = data['text']
        start_time = datetime.now()
        
        pii_analysis = data.get('pii_analysis')
        
        if pii_analysis:
            result = pii_handler.process_query(user_text, pii_analysis)
        else:
            result = pii_handler.process_query(user_text)
        
        # Reconstruct response with original PII
        reconstructed_response = result.get('llm_response', 'No response')
        if pii_analysis and 'allEntities' in pii_analysis:
            for entity in pii_analysis['allEntities']:
                if not entity.get('isDependent', False):
                    # Replace masked values with original values
                    entity_type = entity.get('type', '').upper()
                    original_value = entity.get('value', '')
                    
                    # Replace common masks
                    reconstructed_response = reconstructed_response.replace(f'[{entity_type}]', original_value)
                    reconstructed_response = reconstructed_response.replace('[NAME]', original_value)
                    reconstructed_response = reconstructed_response.replace('[PHONE]', original_value)
                    reconstructed_response = reconstructed_response.replace('[EMAIL]', original_value)
        
        result['final_response'] = reconstructed_response
        
        message = {
            'id': f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(messages.get(session_id, []))}",
            'user_message': user_text,
            'anonymized_text': result.get('masked_query', user_text),
            'bot_response': result.get('llm_response', 'No response'),
            'reconstructed_text': result.get('final_response', result.get('llm_response', 'No response')),
            'privacy_score': result.get('privacy_score', 1.0),
            'processing_time': (datetime.now() - start_time).total_seconds(),
            'timestamp': datetime.now().isoformat(),
            'detected_entities': result.get('detected_entities', []),
            'privacy_preserved': len(result.get('detected_entities', [])) > 0
        }
        
        if session_id not in messages:
            messages[session_id] = []
        messages[session_id].append(message)
        
        sessions[session_id]['updated_at'] = datetime.now().isoformat()
        
        return jsonify(message)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[INFO] Starting server on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
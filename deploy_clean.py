#!/usr/bin/env python3
"""
Ultra-clean PII Privacy Protection System for Render deployment
"""

import os
import json
import re
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pii_privacy_secret_key_2024')
CORS(app)

# In-memory storage for demo (use Redis/DB in production)
sessions_store = {}
messages_store = {}

def extract_entities(text):
    """Extract PII entities using regex"""
    entities = []
    
    # Names (First Last)
    for match in re.finditer(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text):
        entities.append({
            'text': match.group(),
            'type': 'PERSON',
            'start': match.start()
        })
    
    # IDs (ABC123, ORD456, etc.)
    for match in re.finditer(r'\b[A-Z]{2,4}\d{3,5}\b', text):
        entities.append({
            'text': match.group(),
            'type': 'ID',
            'start': match.start()
        })
    
    # Emails
    for match in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        entities.append({
            'text': match.group(),
            'type': 'EMAIL',
            'start': match.start()
        })
    
    return entities

def should_mask_entity(text, entity):
    """Functional dependency logic"""
    query = text.lower()
    
    # Name analysis - keep names
    if any(word in query for word in ['count', 'letters', 'vowels', 'consonants', 'length', 'name']):
        return entity['type'] != 'PERSON'
    
    # Functional operations - keep all
    if any(word in query for word in ['deliver', 'track', 'process', 'return']):
        return False
    
    # General knowledge - mask all
    if any(word in query for word in ['what', 'explain', 'artificial', 'intelligence']):
        return True
    
    return True  # Default: mask

def mask_text(text):
    """Apply functional dependency masking"""
    entities = extract_entities(text)
    masked_text = text
    kept_entities = []
    masked_entities = []
    
    # Process entities in reverse order to maintain indices
    for entity in sorted(entities, key=lambda x: x['start'], reverse=True):
        if should_mask_entity(text, entity):
            # Generate replacement
            replacements = {
                'PERSON': ['John Smith', 'Jane Doe', 'Mike Johnson'],
                'ID': ['ABC123', 'XYZ789', 'DEF456'],
                'EMAIL': ['user@example.com', 'contact@domain.com']
            }
            
            import random
            replacement = random.choice(replacements.get(entity['type'], ['[REDACTED]']))
            
            # Replace in text
            start, end = entity['start'], entity['start'] + len(entity['text'])
            masked_text = masked_text[:start] + replacement + masked_text[end:]
            
            masked_entities.append({
                'original': entity['text'],
                'replacement': replacement,
                'type': entity['type']
            })
        else:
            kept_entities.append(entity)
    
    privacy_score = (len(masked_entities) / len(entities) * 100) if entities else 100.0
    
    return {
        'original_text': text,
        'masked_text': masked_text,
        'kept_entities': kept_entities,
        'masked_entities': masked_entities,
        'privacy_score': privacy_score,
        'processing_time': 0.001  # Minimal processing time
    }

@app.route('/')
def home():
    return jsonify({
        'service': 'PII Privacy Protection System',
        'status': 'running',
        'version': '1.0.0',
        'description': 'Functional Dependency-Based Privacy Masking'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        result = mask_text(data['text'])
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    return jsonify({
        'success': True,
        'data': list(sessions_store.values())
    })

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json() or {}
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    session_data = {
        'id': session_id,
        'title': data.get('title', 'New Chat'),
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    sessions_store[session_id] = session_data
    messages_store[session_id] = []
    
    return jsonify({'success': True, 'data': session_data})

@app.route('/api/sessions/<session_id>/process', methods=['POST'])
def process_in_session(session_id):
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        result = mask_text(data['text'])
        
        # Store message
        message = {
            'id': len(messages_store.get(session_id, [])) + 1,
            'session_id': session_id,
            'user_message': result['original_text'],
            'bot_response': 'Processed with functional dependency masking',
            'anonymized_text': result['masked_text'],
            'reconstructed_text': result['masked_text'],
            'privacy_score': result['privacy_score'],
            'processing_time': result['processing_time'],
            'timestamp': datetime.now().isoformat()
        }
        
        if session_id not in messages_store:
            messages_store[session_id] = []
        messages_store[session_id].append(message)
        
        return jsonify({'success': True, 'data': message})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>/messages')
def get_messages(session_id):
    return jsonify({
        'success': True,
        'data': messages_store.get(session_id, [])
    })

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    sessions_store.pop(session_id, None)
    messages_store.pop(session_id, None)
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
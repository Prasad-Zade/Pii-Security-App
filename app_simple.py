#!/usr/bin/env python3
"""
PII Privacy Protection System - Simplified for Deployment
"""

import os
import json
import re
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'pii_privacy_secret_key_2024'
CORS(app)

class SimplePIISystem:
    def __init__(self):
        print("Simple PII System initialized")
    
    def extract_entities(self, text):
        """Extract entities using regex patterns"""
        entities = []
        
        # Name patterns
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        for name in names:
            entities.append({'text': name, 'type': 'PERSON', 'start': text.find(name)})
        
        # ID patterns
        id_pattern = r'\b[A-Z]{2,4}\d{3,5}\b'
        ids = re.findall(id_pattern, text)
        for id_val in ids:
            entities.append({'text': id_val, 'type': 'ID', 'start': text.find(id_val)})
        
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({'text': email, 'type': 'EMAIL', 'start': text.find(email)})
        
        return entities
    
    def should_mask_entity(self, text, entity):
        """Determine masking based on functional dependency rules"""
        query_lower = text.lower()
        
        # Name analysis queries - keep names
        name_analysis_keywords = [
            'count letters', 'find vowels', 'consonants', 'syllables',
            'starts with', 'ends with', 'contains', 'palindrome',
            'arrange', 'alphabetically', 'compare', 'length'
        ]
        
        # Functional operations - keep all entities
        functional_keywords = [
            'deliver', 'track', 'process', 'return', 'ship',
            'authorize', 'handle', 'complaint', 'transaction'
        ]
        
        # General knowledge - mask all entities
        general_keywords = [
            'what is', 'explain', 'define', 'artificial intelligence',
            'machine learning', 'photosynthesis', 'democracy', 'cooking'
        ]
        
        # Check for functional operations first
        if any(keyword in query_lower for keyword in functional_keywords):
            return False  # Keep all entities
        
        # Check for general knowledge queries
        if any(keyword in query_lower for keyword in general_keywords):
            return True  # Mask all entities
        
        # Check for name analysis
        if any(keyword in query_lower for keyword in name_analysis_keywords):
            if entity['type'] == 'PERSON':
                return False  # Keep names for analysis
            else:
                return True  # Mask non-name entities
        
        return True  # Default: mask for privacy
    
    def generate_replacement(self, entity):
        """Generate replacement for entity"""
        replacements = {
            'PERSON': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson'],
            'ID': ['ABC123', 'XYZ789', 'DEF456', 'GHI012'],
            'EMAIL': ['user@example.com', 'contact@domain.com']
        }
        
        import random
        return random.choice(replacements.get(entity['type'], ['[REDACTED]']))
    
    def process_text(self, text):
        """Process text with functional dependency masking"""
        start_time = datetime.now()
        
        entities = self.extract_entities(text)
        masked_text = text
        kept_entities = []
        masked_entities = []
        
        # Sort entities by position (reverse order)
        entities.sort(key=lambda x: x['start'], reverse=True)
        
        for entity in entities:
            should_mask = self.should_mask_entity(text, entity)
            
            if should_mask:
                replacement = self.generate_replacement(entity)
                masked_text = masked_text.replace(entity['text'], replacement)
                masked_entities.append({
                    'original': entity['text'],
                    'replacement': replacement,
                    'type': entity['type']
                })
            else:
                kept_entities.append(entity)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        privacy_score = (len(masked_entities) / len(entities) * 100) if entities else 100.0
        
        return {
            'original_text': text,
            'masked_text': masked_text,
            'kept_entities': kept_entities,
            'masked_entities': masked_entities,
            'processing_time': processing_time,
            'privacy_score': privacy_score
        }

# Initialize system
pii_system = SimplePIISystem()

@app.route('/')
def index():
    return jsonify({
        'service': 'PII Privacy Protection System',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'process': '/api/process',
            'health': '/api/health',
            'sessions': '/api/sessions'
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'PII Privacy Protection System',
        'version': '1.0.0',
        'model_loaded': True
    })

@app.route('/api/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        result = pii_system.process_text(text)
        
        # Store in session
        if 'history' not in session:
            session['history'] = []
        
        session['history'].append({
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
        
        session['history'] = session['history'][-10:]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    history = session.get('history', [])
    sessions = []
    
    for h in history:
        sessions.append({
            'id': h['id'],
            'title': h['result']['original_text'][:50] + '...' if len(h['result']['original_text']) > 50 else h['result']['original_text'],
            'created_at': h['timestamp'],
            'updated_at': h['timestamp']
        })
    
    return jsonify({'success': True, 'data': sessions})

@app.route('/api/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    title = data.get('title', 'New Chat')
    
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'data': {
            'id': session_id,
            'title': title,
            'created_at': timestamp,
            'updated_at': timestamp
        }
    })

@app.route('/api/sessions/<session_id>/process', methods=['POST'])
def process_text_in_session(session_id):
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        result = pii_system.process_text(text)
        
        if 'history' not in session:
            session['history'] = []
        
        message_data = {
            'id': session_id,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        session['history'].append(message_data)
        session['history'] = session['history'][-50:]
        
        response_data = {
            'id': len(session['history']),
            'session_id': session_id,
            'user_message': result['original_text'],
            'bot_response': 'Text processed with functional dependency-based privacy masking.',
            'anonymized_text': result['masked_text'],
            'reconstructed_text': result['masked_text'],
            'privacy_score': result['privacy_score'],
            'processing_time': result['processing_time'],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({'success': True, 'data': response_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    if 'history' in session:
        session['history'] = [h for h in session['history'] if h['id'] != session_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting PII Privacy Protection System")
    print(f"Web Interface: http://0.0.0.0:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)
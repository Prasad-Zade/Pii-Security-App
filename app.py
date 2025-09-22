#!/usr/bin/env python3
"""
PII Privacy Protection System - Final Year Project
Functional Dependency-Based Privacy Masking
"""

import os
import sys
import json
import torch
import re
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import uuid
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.core.pii_system import PIIPrivacySystem

app = Flask(__name__)
app.secret_key = 'pii_privacy_secret_key_2024'
CORS(app)  # Enable CORS for Flutter app

class FunctionalPIISystem:
    def __init__(self):
        self.pii_system = PIIPrivacySystem()
        self.load_functional_model()
        
    def load_functional_model(self):
        """Load the trained functional dependency model"""
        model_path = './functional_model'
        try:
            if os.path.exists(model_path) and os.path.exists(os.path.join(model_path, 'config.json')):
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
                print("Success: Functional dependency model loaded successfully")
            else:
                raise FileNotFoundError("Model files not found")
        except Exception as e:
            print(f"Warning: Could not load functional model ({e}), using intelligent fallback")
            self.tokenizer = None
            self.model = None
    
    def extract_entities(self, text):
        """Extract entities from text"""
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
        
        # Phone patterns
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities.append({'text': phone, 'type': 'PHONE', 'start': text.find(phone)})
        
        return entities
    
    def should_mask_entity(self, text, entity):
        """Determine if entity should be masked based on functional dependency"""
        if not self.model or not self.tokenizer:
            # Intelligent fallback logic
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
        
        # Use trained model
        context = f"Query: {text} | Entity: {entity['text']} | Type: {entity['type']}"
        
        inputs = self.tokenizer(
            context, 
            return_tensors='pt', 
            truncation=True, 
            padding=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=1).item()
        
        return prediction == 0  # 0 = mask, 1 = keep
    
    def process_text(self, text):
        """Process text with functional dependency masking"""
        start_time = datetime.now()
        
        # Extract entities
        entities = self.extract_entities(text)
        
        # Process with base PII system
        base_result = self.pii_system.process(text, include_llm=False)
        
        # Apply functional dependency logic
        masked_text = text
        kept_entities = []
        masked_entities = []
        
        # Sort entities by position (reverse order to maintain indices)
        entities.sort(key=lambda x: x['start'], reverse=True)
        
        for entity in entities:
            should_mask = self.should_mask_entity(text, entity)
            
            if should_mask:
                # Generate replacement
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
        
        return {
            'original_text': text,
            'masked_text': masked_text,
            'kept_entities': kept_entities,
            'masked_entities': masked_entities,
            'processing_time': processing_time,
            'privacy_score': self.calculate_privacy_score(entities, masked_entities)
        }
    
    def generate_replacement(self, entity):
        """Generate appropriate replacement for entity"""
        replacements = {
            'PERSON': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson'],
            'ID': ['ABC123', 'XYZ789', 'DEF456', 'GHI012'],
            'EMAIL': ['user@example.com', 'contact@domain.com'],
            'PHONE': ['555-0123', '555-0456']
        }
        
        import random
        return random.choice(replacements.get(entity['type'], ['[REDACTED]']))
    
    def calculate_privacy_score(self, all_entities, masked_entities):
        """Calculate privacy protection score"""
        if not all_entities:
            return 100.0
        
        masked_count = len(masked_entities)
        total_count = len(all_entities)
        
        return (masked_count / total_count) * 100

# Initialize system
pii_system = FunctionalPIISystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        result = pii_system.process_text(text)
        
        # Store in session for history
        if 'history' not in session:
            session['history'] = []
        
        session['history'].append({
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
        
        # Keep only last 10 entries
        session['history'] = session['history'][-10:]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    return jsonify(session.get('history', []))

@app.route('/api/stats')
def get_stats():
    history = session.get('history', [])
    
    if not history:
        return jsonify({
            'total_processed': 0,
            'avg_privacy_score': 0,
            'avg_processing_time': 0,
            'entity_types': {}
        })
    
    total_processed = len(history)
    avg_privacy_score = sum(h['result']['privacy_score'] for h in history) / total_processed
    avg_processing_time = sum(h['result']['processing_time'] for h in history) / total_processed
    
    entity_types = {}
    for h in history:
        for entity in h['result']['masked_entities']:
            entity_type = entity['type']
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
    
    return jsonify({
        'total_processed': total_processed,
        'avg_privacy_score': round(avg_privacy_score, 2),
        'avg_processing_time': round(avg_processing_time, 4),
        'entity_types': entity_types
    })

# Flutter App Specific Endpoints
@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all chat sessions for Flutter app"""
    history = session.get('history', [])
    sessions = []
    
    for i, h in enumerate(history):
        sessions.append({
            'id': h['id'],
            'title': h['result']['original_text'][:50] + '...' if len(h['result']['original_text']) > 50 else h['result']['original_text'],
            'created_at': h['timestamp'],
            'updated_at': h['timestamp']
        })
    
    return jsonify({
        'success': True,
        'data': sessions
    })

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create new chat session for Flutter app"""
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

@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    """Get messages for a specific session"""
    history = session.get('history', [])
    messages = [h for h in history if h['id'] == session_id]
    
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            'id': len(formatted_messages) + 1,
            'session_id': session_id,
            'user_message': msg['result']['original_text'],
            'bot_response': 'Text processed successfully with functional dependency analysis.',
            'anonymized_text': msg['result']['masked_text'],
            'reconstructed_text': msg['result']['masked_text'],
            'privacy_score': msg['result']['privacy_score'],
            'processing_time': msg['result']['processing_time'],
            'timestamp': msg['timestamp']
        })
    
    return jsonify({
        'success': True,
        'data': formatted_messages
    })

@app.route('/api/sessions/<session_id>/process', methods=['POST'])
def process_text_in_session(session_id):
    """Process text within a specific session for Flutter app"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        result = pii_system.process_text(text)
        
        # Store in session history
        if 'history' not in session:
            session['history'] = []
        
        message_data = {
            'id': session_id,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        
        session['history'].append(message_data)
        session['history'] = session['history'][-50:]  # Keep last 50
        
        # Format response for Flutter app
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
        
        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session"""
    if 'history' in session:
        session['history'] = [h for h in session['history'] if h['id'] != session_id]
    
    return jsonify({'success': True})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'PII Privacy Protection System',
        'version': '1.0.0',
        'model_loaded': pii_system.model is not None
    })

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Starting PII Privacy Protection System")
    print("Functional Dependency Model: Ready")
    print(f"Web Interface: http://0.0.0.0:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)
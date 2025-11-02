"""
PII Dependency Handler - Simplified for deployment
"""

import re
import requests
from typing import Dict, Any, List

class PIIDependencyHandler:
    def __init__(self):
        self.api_key = 'AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo'
        
    def process_query(self, user_query: str, pii_analysis: Dict = None) -> Dict[str, Any]:
        """Process query with PII handling"""
        
        if pii_analysis:
            masked = pii_analysis.get('maskedQuery', user_query)
            entities = pii_analysis.get('allEntities', [])
        else:
            masked, entities = self._simple_mask(user_query)
        
        response = self._generate_response(masked)
        
        # Reconstruct response with original PII
        reconstructed = response
        if pii_analysis and 'allEntities' in pii_analysis:
            for entity in pii_analysis['allEntities']:
                if not entity.get('isDependent', False):
                    entity_type = entity.get('type', '').lower()
                    original_value = entity.get('value', '')
                    masked_value = entity.get('maskedValue', '')
                    
                    # Replace fake values and masks with original values
                    if masked_value and masked_value in reconstructed:
                        reconstructed = reconstructed.replace(masked_value, original_value)
                    
                    # Also replace common placeholder patterns
                    reconstructed = reconstructed.replace(f'[{entity_type.upper()}]', original_value)
                    
                    # Replace specific fake names with original
                    if entity_type == 'name':
                        fake_names = ['John Smith', 'Jane Doe', 'Alex Johnson', 'Sarah Wilson']
                        for fake_name in fake_names:
                            if fake_name in reconstructed:
                                reconstructed = reconstructed.replace(fake_name, original_value)
                                break
        
        # Calculate proper privacy score
        privacy_score = 100.0
        if pii_analysis and 'allEntities' in pii_analysis:
            total_entities = len(pii_analysis['allEntities'])
            if total_entities > 0:
                privacy_score = max(20.0, 100.0 - (total_entities * 15))
        elif entities:
            privacy_score = max(20.0, 100.0 - (len(entities) * 15))
        
        return {
            'original_query': user_query,
            'masked_query': masked,
            'detected_entities': entities,
            'llm_response': response,
            'final_response': reconstructed,
            'privacy_score': privacy_score
        }
    
    def _simple_mask(self, text: str) -> tuple:
        """Simple PII masking"""
        patterns = {
            'phone': r'\b\d{10}\b',
            'email': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        }
        
        masked = text
        detected = []
        
        for pii_type, pattern in patterns.items():
            if re.search(pattern, text):
                detected.append(pii_type)
                masked = re.sub(pattern, f'[{pii_type.upper()}]', masked)
        
        return masked, detected
    
    def _generate_response(self, text: str) -> str:
        """Generate response using Gemini API"""
        
        # Try Gemini API for all queries
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.api_key}'
            
            response = requests.post(url, json={
                'contents': [{'parts': [{'text': text}]}],
                'generationConfig': {
                    'maxOutputTokens': 512,
                    'temperature': 0.7
                }
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
        except Exception as e:
            print(f"[INFO] API error: {e}")
        
        return "I understand your message. How can I help you further?"
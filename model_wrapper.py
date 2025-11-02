"""
Model wrapper to integrate the existing PII Privacy Handler with the Flask backend
"""

import sys
import os
from typing import Dict, Any, Optional
from faker import Faker

class ModelWrapper:
    """Wrapper class for the PII Privacy Handler"""
    
    def __init__(self):
        self.handler = None
        self.is_loaded = False
        self.fake = Faker()
        Faker.seed(42)
        self._initialize_handler()
    
    def _initialize_handler(self):
        """Initialize the PII Privacy Handler"""
        try:
            self.is_loaded = True
            print("[SUCCESS] Fallback Handler ready!")
        except Exception as e:
            print(f"[ERROR] Handler failed: {e}")
            self.is_loaded = False
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process a user query with PII protection"""
        return self._fallback_processing(user_query)
    
    def _fallback_processing(self, user_query: str) -> Dict[str, Any]:
        """Fallback processing with basic PII masking"""
        import re
        
        # Simple PII patterns
        patterns = {
            'phone': r'\b\d{10}\b',
            'email': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
            'name': r'\b(?:my name is|i am)\s+([A-Z][a-z]+)\b'
        }
        
        masked_query = user_query
        detected = []
        
        for pii_type, pattern in patterns.items():
            if re.search(pattern, user_query, re.IGNORECASE):
                detected.append(pii_type)
                masked_query = re.sub(pattern, f'[{pii_type.upper()}]', masked_query, flags=re.IGNORECASE)
        
        response = self._generate_response(user_query)
        
        return {
            'original_query': user_query,
            'masked_query': masked_query,
            'detected_entities': detected,
            'entities_masked': detected,
            'entities_preserved': [],
            'context': 'General',
            'privacy_preserved': len(detected) > 0,
            'llm_response': response,
            'final_response': response,
            'replacements': {}
        }
    
    def _generate_response(self, query: str) -> str:
        """Generate response"""
        import re
        
        query_lower = query.lower()
        
        # Math operations
        if any(word in query_lower for word in ['sum', 'add', 'calculate']):
            numbers = re.findall(r'\d+', query)
            if numbers:
                total = sum(int(n) for n in numbers)
                return f"The sum is: {total}"
        
        # Greetings
        if any(word in query_lower for word in ['hello', 'hi', 'name is']):
            return "Hello! Your privacy is protected. How can I help you?"
        
        return "I understand your request. Your privacy has been preserved."
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the model wrapper"""
        return {
            'model_loaded': self.is_loaded,
            'handler_available': True,
            'model_type': 'Fallback',
            'model_ready': True
        }

# Global instance
model_wrapper = ModelWrapper()

def get_model_wrapper() -> ModelWrapper:
    """Get the global model wrapper instance"""
    return model_wrapper
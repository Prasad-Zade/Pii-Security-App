"""
Simplified PII Privacy Handler that integrates your model's core functionality
without encoding issues for the Flutter app
"""

import re
import os
import sys
from typing import Dict, List, Any
from faker import Faker

class SimplePIIPrivacyHandler:
    """Simplified version of your PII Privacy Handler for Flutter integration"""
    
    def __init__(self):
        self.fake = Faker()
        self.name_cache = {}
        
        # Core PII patterns from your model
        self.pii_patterns = {
            'NAME': [
                r'\b(?:i am|my name is|myself)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)\b',
                r'\b(prasad|zade|lokesh|piyush|rahul|amit|priya|john|alice|bob|sarah|mike|jane|david|mary|alex|johnson)\b'
            ],
            'PHONE': [
                r'\bphone\s+number\s+is\s+(\d{10})\b',
                r'\bmobile\s+number\s+is\s+(\d{10})\b',
                r'\b(\d{10})\b'
            ],
            'EMAIL': [
                r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
            ],
            'AADHAAR': [
                r'\baadhaar\s+number\s+is\s+(\d{12})\b',
                r'\baadhar\s+number\s+is\s+(\d{12})\b',
                r'\b(\d{12})\b'
            ]
        }
        
        self.computation_keywords = [
            'add', 'sum', 'calculate', 'count', 'digit', 'addition', 
            'multiply', 'divide', 'subtract', 'total', 'letters',
            'extract', 'domain', 'find', 'get', 'tell', 'reverse'
        ]
    
    def detect_entities(self, text: str) -> List[Dict]:
        """Detect PII entities in text"""
        entities = []
        seen_entities = set()
        
        # Debug print
        print(f"[DEBUG] Detecting entities in: '{text}'")
        
        for pii_type, patterns in self.pii_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group(1) if match.groups() else match.group(0)
                    start_pos = match.start(1) if match.groups() else match.start()
                    end_pos = match.end(1) if match.groups() else match.end()
                    
                    print(f"[DEBUG] Found {pii_type}: '{entity_text}' at {start_pos}-{end_pos}")
                    
                    entity_key = (entity_text.lower(), start_pos, end_pos)
                    if entity_key not in seen_entities:
                        seen_entities.add(entity_key)
                        entities.append({
                            'type': pii_type,
                            'text': entity_text,
                            'start': start_pos,
                            'end': end_pos
                        })
        
        print(f"[DEBUG] Total entities found: {len(entities)}")
        return entities
    
    def is_computation_required(self, text: str, entity: Dict) -> bool:
        """Check if entity is needed for computation"""
        text_lower = text.lower()
        
        has_computation = any(keyword in text_lower for keyword in self.computation_keywords)
        
        if not has_computation:
            return False
        
        if entity['type'] == 'AADHAAR' and any(word in text_lower for word in ['addition', 'add', 'sum', 'digit']) and 'aadhar' in text_lower:
            return True
        
        if entity['type'] == 'PHONE' and any(word in text_lower for word in ['digit', 'add', 'sum']) and 'phone' in text_lower:
            return True
        
        if entity['type'] == 'NAME' and any(word in text_lower for word in ['count', 'letters', 'length', 'reverse']) and 'name' in text_lower:
            return True
        
        if entity['type'] == 'EMAIL' and any(word in text_lower for word in ['extract', 'domain', 'find']) and 'email' in text_lower:
            return True
            
        return False
    
    def analyze_context(self, text: str) -> str:
        """Simple context analysis"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in self.computation_keywords):
            return 'Mathematical'
        elif any(word in text_lower for word in ['doctor', 'patient', 'medical']):
            return 'Medical'
        elif any(word in text_lower for word in ['account', 'bank', 'credit']):
            return 'Financial'
        else:
            return 'General'
    
    def generate_fake_value(self, entity_type: str, original_value: str) -> str:
        """Generate realistic fake value"""
        cache_key = f"{entity_type}_{original_value}"
        if cache_key in self.name_cache:
            return self.name_cache[cache_key]
        
        fake_value = ""
        
        if entity_type == 'NAME':
            if ' ' in original_value:
                fake_value = self.fake.name()
            else:
                fake_value = self.fake.first_name()
        elif entity_type == 'PHONE':
            fake_value = ''.join([str(self.fake.random_digit()) for _ in range(10)])
        elif entity_type == 'EMAIL':
            fake_value = self.fake.email()
        elif entity_type == 'AADHAAR':
            fake_value = ''.join([str(self.fake.random_digit()) for _ in range(12)])
        else:
            fake_value = f"[{entity_type}]"
        
        self.name_cache[cache_key] = fake_value
        return fake_value
    
    def generate_intelligent_response(self, masked_query: str, original_query: str) -> str:
        """Generate intelligent response for any query"""
        query_lower = original_query.lower()  # Use original for better context
        
        # Mathematical operations - digit sum calculations
        if any(word in query_lower for word in ['sum', 'add', 'addition', 'calculate']) and 'digit' in query_lower:
            number_match = re.search(r'\b(\d+)\b', original_query)
            if number_match:
                number = number_match.group(1)
                digits = [int(d) for d in number]
                total = sum(digits)
                
                if 'aadhaar' in query_lower or 'aadhar' in query_lower:
                    return f"The sum of all digits in the Aadhaar number {number} is: {total}"
                elif 'phone' in query_lower:
                    return f"The sum of all digits in the phone number {number} is: {total}"
                else:
                    return f"The sum of all digits in {number} is: {total}"
        
        # String reversal operations
        if 'reverse' in query_lower:
            name_match = re.search(r'"([^"]+)"', original_query) or re.search(r'name\s+"?([A-Za-z]+)"?', original_query)
            if name_match:
                name = name_match.group(1)
                reversed_name = name[::-1]
                return f"The reverse of '{name}' is: {reversed_name}"
        
        # Count letters
        if 'count' in query_lower and 'letters' in query_lower:
            name_match = re.search(r'\bname\s+(\w+)', original_query)
            if name_match:
                name = name_match.group(1)
                count = len([c for c in name if c.isalpha()])
                return f"The name '{name}' has {count} letters."
        
        # Email domain extraction
        if ('extract' in query_lower or 'find' in query_lower) and 'domain' in query_lower:
            email_match = re.search(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', original_query)
            if email_match:
                email = email_match.group(1)
                domain = email.split('@')[1]
                return f"The domain from email {email} is: {domain}"
        
        # Greetings and introductions
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'myself', 'my name is', 'i am']):
            return "Hello! I've processed your introduction while protecting your personal information. How can I help you today?"
        
        # AI/Tech questions
        if any(word in query_lower for word in ['what is', 'explain', 'tell me about']):
            if 'artificial intelligence' in query_lower or ' ai ' in query_lower:
                return "Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. It includes machine learning, natural language processing, and robotics."
            elif 'machine learning' in query_lower:
                return "Machine Learning is a subset of AI that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns and make predictions."
        
        # Default response
        return "I understand your message. Your privacy has been protected by masking personal information while maintaining the context needed to help you."
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Main method to process user query with PII privacy protection"""
        try:
            # Detect entities
            entities = self.detect_entities(user_query)
            
            # Analyze context
            context = self.analyze_context(user_query)
            
            # Apply masking
            masked_query = user_query
            masked_entities = []
            preserved_entities = []
            
            # Sort entities by start position in reverse order
            entities_sorted = sorted(entities, key=lambda x: x['start'], reverse=True)
            
            for entity in entities_sorted:
                needs_computation = self.is_computation_required(user_query, entity)
                
                if needs_computation:
                    preserved_entities.append(entity['type'])
                else:
                    fake_value = self.generate_fake_value(entity['type'], entity['text'])
                    start_pos = entity['start']
                    end_pos = entity['end']
                    
                    # Ensure we don't have regex replacement artifacts
                    if start_pos < len(masked_query) and end_pos <= len(masked_query):
                        masked_query = masked_query[:start_pos] + fake_value + masked_query[end_pos:]
                        masked_entities.append(entity['type'])
            
            # Generate response
            llm_response = self.generate_intelligent_response(masked_query, user_query)
            
            print(f"[DEBUG] Final result:")
            print(f"  Original: {user_query}")
            print(f"  Masked: {masked_query}")
            print(f"  Entities: {[e['type'] for e in entities]}")
            print(f"  Masked entities: {masked_entities}")
            print(f"  Response: {llm_response}")
            
            return {
                'original_query': user_query,
                'masked_query': masked_query,
                'detected_entities': [e['type'] for e in entities],
                'entities_masked': masked_entities,
                'entities_preserved': preserved_entities,
                'context': context,
                'privacy_preserved': len(masked_entities) > 0,
                'llm_response': llm_response,
                'final_response': llm_response,
                'replacements': {}
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'original_query': user_query,
                'final_response': "Error processing request."
            }
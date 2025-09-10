import pickle
import numpy as np
from typing import List, Dict, Any
import os

class MLDependencyAnalyzer:
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_path = model_path or os.path.join(os.path.dirname(__file__), '..', '..', 'training', 'pii_model.pkl')
        self.load_model()
    
    def load_model(self):
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data['classifier']
                print("ML model loaded successfully")
            else:
                print(f"Model not found at {self.model_path}, using rule-based fallback")
        except Exception as e:
            print(f"Error loading model: {e}, using rule-based fallback")
    
    def extract_features(self, text: str, entity: Any) -> np.ndarray:
        """Extract features for ML prediction"""
        text_lower = text.lower()
        entity_text = entity.text.lower()
        
        # Mathematical context
        has_calculate = 'calculate' in text_lower
        has_addition = 'addition' in text_lower or 'sum' in text_lower
        has_count = 'count' in text_lower
        has_tell_me = 'tell me' in text_lower
        
        # Entity type features
        is_person = entity.label == 'PERSON'
        is_phone = entity.label == 'PHONE'
        is_aadhaar = entity.label == 'AADHAAR'
        is_medical = entity.label == 'MEDICAL_CONDITION'
        
        # Position features
        entity_pos = text_lower.find(entity_text)
        entity_position = entity_pos / len(text) if len(text) > 0 else 0
        
        # Context window features
        window_size = 50
        start_window = max(0, entity_pos - window_size)
        end_window = min(len(text), entity_pos + len(entity_text) + window_size)
        context = text_lower[start_window:end_window] if entity_pos >= 0 else text_lower
        
        context_has_my = 'my' in context
        context_has_is = ' is ' in context
        context_has_number = 'number' in context
        
        return np.array([[
            has_calculate, has_addition, has_count, has_tell_me,
            is_person, is_phone, is_aadhaar, is_medical,
            entity_position, context_has_my, context_has_is, context_has_number
        ]])
    
    def should_preserve_entity(self, entity: Any, text: str) -> bool:
        """Use ML model to determine if entity should be preserved"""
        
        # Always preserve medical conditions
        if entity.label == 'MEDICAL_CONDITION':
            return True
        
        # Use ML model if available
        if self.model:
            try:
                features = self.extract_features(text, entity)
                prediction = self.model.predict(features)[0]
                return bool(prediction)
            except Exception as e:
                print(f"ML prediction error: {e}, falling back to rules")
        
        # Fallback to rule-based approach
        return self._rule_based_decision(entity, text)
    
    def _rule_based_decision(self, entity: Any, text: str) -> bool:
        """Fallback rule-based decision"""
        text_lower = text.lower()
        
        # Preserve for calculation contexts
        calc_patterns = [
            'calculate', 'addition', 'sum', 'total', 'count', 'tell me addition'
        ]
        
        if any(pattern in text_lower for pattern in calc_patterns):
            # Don't preserve names even in calculation context
            if entity.label == 'PERSON':
                return False
            # Preserve numbers for calculation
            if entity.label in ['PHONE', 'AADHAAR', 'PAN']:
                return True
        
        return False
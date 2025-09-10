#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_fresh():
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    # Test the exact case you mentioned
    test_cases = [
        "my name is prasad and my phone number is 1111111111",
        "My name is John and my phone is 9876543210", 
        "I am Ankit, phone: 1234567890",
        "Name: Riya, Phone: 9988776655"
    ]
    
    for text in test_cases:
        print(f"\nInput: {text}")
        entities = detector.detect_entities(text)
        print(f"Entities: {[(e.label, e.text, e.preserve) for e in entities]}")
        result = anonymizer.anonymize_text(text, entities)[0]
        print(f"Output: {result}")

if __name__ == "__main__":
    test_fresh()
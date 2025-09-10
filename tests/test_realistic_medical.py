#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_realistic_medical():
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        "My name is Prasad and I have diabetes",
        "John has cancer, phone: 9876543210", 
        "Count letters in the name Ankit Sharma",
        "Add 1000 to 9876543210"
    ]
    
    for text in test_cases:
        print(f"\nInput: {text}")
        entities = detector.detect_entities(text)
        print(f"Entities: {[(e.label, e.text, e.preserve) for e in entities]}")
        result = anonymizer.anonymize_text(text, entities)[0]
        print(f"Output: {result}")

if __name__ == "__main__":
    test_realistic_medical()
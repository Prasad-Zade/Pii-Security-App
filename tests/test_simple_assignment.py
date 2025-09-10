#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_simple_assignment():
    """Test simple PII assignment cases that should be anonymized"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    text = "my name is prasad and my phone number is 1111111111"
    entities = detector.detect_entities(text)
    
    print(f"Input: {text}")
    print(f"Entities found: {len(entities)}")
    for e in entities:
        print(f"  - {e.label}: '{e.text}' at {e.start}-{e.end}, preserve={e.preserve}")
    
    result, mapping = anonymizer.anonymize_text(text, entities)
    print(f"Result: {result}")
    print(f"Expected: my name is [NAME] and my phone number is [PHONE]")

if __name__ == "__main__":
    test_simple_assignment()
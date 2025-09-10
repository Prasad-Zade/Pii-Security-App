#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_mixed_context():
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    entities = detector.detect_entities(text)
    
    print(f"Input: {text}")
    print(f"Entities found: {len(entities)}")
    for e in entities:
        print(f"  - {e.label}: '{e.text}' at {e.start}-{e.end}, preserve={e.preserve}")
    
    result = anonymizer.anonymize_text(text, entities)[0]
    print(f"Result: {result}")
    print(f"Expected: my name is [FAKE_NAME] and my phone number is 1111111111 tell me addition of it")

if __name__ == "__main__":
    test_mixed_context()
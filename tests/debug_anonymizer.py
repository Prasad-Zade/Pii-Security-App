#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def debug_test():
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    text = "My name is Prasad Zade"
    entities = detector.detect_entities(text)
    
    print(f"Input: {text}")
    print(f"Entities found: {len(entities)}")
    for e in entities:
        print(f"  - {e.label}: '{e.text}' at {e.start}-{e.end}, preserve={e.preserve}")
    
    result, mapping = anonymizer.anonymize_text(text, entities)
    print(f"Result: {result}")
    print(f"Mapping: {mapping}")

if __name__ == "__main__":
    debug_test()
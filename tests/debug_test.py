#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def debug_specific_input():
    pii_system = PIIPrivacySystem()
    
    test_text = "my name is prasad zade"
    print(f"Input: {test_text}")
    print("-" * 40)
    
    # Get detailed info
    entities = pii_system.detector.detect_entities(test_text)
    print(f"Detected entities: {len(entities)}")
    for i, entity in enumerate(entities):
        print(f"  {i+1}. Text: '{entity.text}' | Label: {entity.label} | Start: {entity.start} | End: {entity.end}")
    
    result = pii_system.process(test_text, include_llm=False)
    print(f"\nOriginal: {result.original_text}")
    print(f"Anonymized: {result.anonymized_text}")
    print(f"Privacy Score: {result.privacy_score}")

if __name__ == "__main__":
    debug_specific_input()
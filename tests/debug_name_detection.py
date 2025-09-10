#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.enhanced_detector import EnhancedPIIDetector

def debug_name_detection():
    detector = EnhancedPIIDetector()
    
    test_text = "my name is prasad zade and my phone number is 1478523697"
    print(f"Testing: {test_text}")
    
    entities = detector.detect_entities(test_text)
    print(f"Detected entities: {len(entities)}")
    
    for entity in entities:
        print(f"  -> {entity.label}: '{entity.text}' at {entity.start}-{entity.end}")
    
    # Test the specific pattern
    import re
    pattern = re.compile(r'\b(?:my name is|i am|i\'m|called|name:|full name)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)+)', re.IGNORECASE)
    matches = pattern.finditer(test_text)
    
    print("\nPattern matches:")
    for match in matches:
        print(f"  -> Full match: '{match.group(0)}'")
        print(f"  -> Name part: '{match.group(1)}'")
        print(f"  -> Position: {match.start(1)}-{match.end(1)}")

if __name__ == "__main__":
    debug_name_detection()
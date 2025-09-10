#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_phone_computation():
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    entity_value = "1111111111"
    entity_lower = entity_value.lower()
    text_lower = text.lower()
    
    # Test computational patterns for phone
    computational_patterns = [
        rf'(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
        rf'{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\b',
        rf'(?:calculate|compute)\s+(?:the\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
        rf'(?:number|phone|card)\s+is\s+{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?(?:it|this)',
    ]
    
    print(f"Text: {text_lower}")
    print(f"Entity (phone): {entity_lower}")
    
    for i, pattern in enumerate(computational_patterns):
        print(f"\nPattern {i}: {pattern}")
        match = re.search(pattern, text_lower)
        print(f"Match: {match}")
        if match:
            print(f"Matched text: '{match.group()}'")

if __name__ == "__main__":
    test_phone_computation()
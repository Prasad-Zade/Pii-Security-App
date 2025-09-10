#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_phone_exclusion():
    text = "my name is prasad and my phone number is 1111111111"
    entity_value = "1111111111"
    entity_lower = entity_value.lower()
    text_lower = text.lower()
    
    exclude_patterns = [
        rf'(?:my|his|her|their)\s+(?:phone|mobile|contact)\s+(?:number\s+)?(?:is\s+)?{re.escape(entity_lower)}',
    ]
    
    print(f"Text: {text_lower}")
    print(f"Entity: {entity_lower}")
    
    for i, pattern in enumerate(exclude_patterns):
        print(f"Pattern {i}: {pattern}")
        match = re.search(pattern, text_lower)
        print(f"Match: {match}")
        if match:
            print(f"Matched text: '{match.group()}'")

if __name__ == "__main__":
    test_phone_exclusion()
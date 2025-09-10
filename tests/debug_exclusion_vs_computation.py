#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_exclusion_vs_computation():
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    entity_value = "1111111111"
    entity_lower = entity_value.lower()
    text_lower = text.lower()
    
    # Exclusion patterns
    exclude_patterns = [
        rf'(?:my|his|her|their)\s+(?:phone|mobile|contact)\s+(?:number\s+)?(?:is\s+)?{re.escape(entity_lower)}\b',
        rf'(?:phone|mobile|contact)\s+(?:number\s+)?(?:is\s+)?{re.escape(entity_lower)}\b',
    ]
    
    # Computational patterns
    computational_patterns = [
        rf'{re.escape(entity_lower)}.*(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?(?:it|this)',
    ]
    
    print("=== EXCLUSION PATTERNS ===")
    excluded = False
    for i, pattern in enumerate(exclude_patterns):
        match = re.search(pattern, text_lower)
        print(f"Pattern {i}: {pattern}")
        print(f"Match: {match}")
        if match:
            excluded = True
            print(f"EXCLUDED by pattern {i}")
    
    print("\n=== COMPUTATIONAL PATTERNS ===")
    computational = False
    for i, pattern in enumerate(computational_patterns):
        match = re.search(pattern, text_lower)
        print(f"Pattern {i}: {pattern}")
        print(f"Match: {match}")
        if match:
            computational = True
            print(f"COMPUTATIONAL by pattern {i}")
    
    print(f"\nExcluded: {excluded}")
    print(f"Computational: {computational}")
    print(f"Should preserve: {computational and not excluded}")

if __name__ == "__main__":
    test_exclusion_vs_computation()
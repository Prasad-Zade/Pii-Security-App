#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_all_name_patterns():
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    entity_value = "prasad"
    entity_lower = entity_value.lower()
    text_lower = text.lower()
    
    # All computational patterns from the code
    computational_patterns = [
        # Mathematical operations with numbers
        rf'(?:add|sum|total|multiply|divide|subtract)\s+\d+\s+(?:to|and|with)\s+{re.escape(entity_lower)}',
        rf'(?:add|sum|total|multiply|divide|subtract)\s+{re.escape(entity_lower)}\s+(?:to|and|with)\s+\d+',
        rf'{re.escape(entity_lower)}\s*[\+\-\*\/×÷]\s*\d+',
        rf'\d+\s*[\+\-\*\/×÷]\s*{re.escape(entity_lower)}',
        
        # Counting and character analysis
        rf'count\s+(?:letters|characters|digits)\s+in\s+(?:the\s+name\s+)?{re.escape(entity_lower)}',
        rf'(?:how\s+many\s+)?(?:letters|characters|digits)\s+(?:are\s+)?(?:in\s+|before\s+@\s+in\s+)?{re.escape(entity_lower)}',
        rf'(?:length|size)\s+of\s+{re.escape(entity_lower)}',
        
        # Addition/calculation requests (more specific)
        rf'(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
        rf'{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\b',
        rf'(?:calculate|compute)\s+(?:the\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
        rf'{re.escape(entity_lower)}\s*(?:\+|plus)\s*\d+',
        rf'\d+\s*(?:\+|plus)\s*{re.escape(entity_lower)}',
        rf'(?:number|phone|card)\s+is\s+{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?(?:it|this)',
        
        # Format validation and checking
        rf'check\s+if\s+{re.escape(entity_lower)}\s+(?:has|contains|follows|passes|is)',
        rf'(?:does\s+)?{re.escape(entity_lower)}\s+(?:have|contain|follow|pass|match)\s+(?:correct|\d+)',
        rf'(?:validate|verify)\s+{re.escape(entity_lower)}\s+(?:format|algorithm)',
    ]
    
    print(f"Text: {text_lower}")
    print(f"Entity (name): {entity_lower}")
    
    for i, pattern in enumerate(computational_patterns):
        match = re.search(pattern, text_lower)
        if match:
            print(f"\nMATCH - Pattern {i}: {pattern}")
            print(f"Matched text: '{match.group()}'")

if __name__ == "__main__":
    test_all_name_patterns()
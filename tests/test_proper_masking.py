#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_proper_masking():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Case 1: No calculation - should mask EVERYTHING
        "my name is prasad zade and my phone number is 1478523697",
        
        # Case 2: With calculation - should preserve ONLY phone, mask name
        "my name is prasad zade and my phone number is 7418529632 and tell me addition of it",
        
        # Case 3: More examples
        "I am John Smith, email john@gmail.com, phone 9876543210",
        "Name: Alice Brown, Phone: 5555555555, what is sum of 5555555555?",
    ]
    
    print("Proper PII Masking Test")
    print("=" * 60)
    print("RULE: Replace ALL PII with FAKE data unless referenced in calculations")
    print()
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"{i}. Input: {test_text}")
        print(f"   Entities: {len(result.entities)}")
        
        for entity in result.entities:
            if hasattr(entity, 'preserve') and entity.preserve:
                print(f"   -> PRESERVED: {entity.label}: '{entity.text}' (calculation reference)")
            else:
                print(f"   -> MASKED: {entity.label}: '{entity.text}' -> FAKE DATA")
        
        print(f"   Masked Result: {result.anonymized_text}")
        print(f"   Should show FAKE names/phones, not real ones!")
        print()

if __name__ == "__main__":
    test_proper_masking()
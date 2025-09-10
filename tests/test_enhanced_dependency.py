#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_enhanced_dependency():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Case 1: No calculation - should anonymize both
        "My name is prasad zade and my phone number is 1478523697",
        
        # Case 2: With calculation - should preserve phone, anonymize name
        "My name is prasad zade and my phone number is 7418529632 and tell me addition of it",
        
        # Case 3: Multiple calculations
        "My phone is 9876543210, name is John Doe, what is sum of 9876543210?",
        
        # Case 4: Different calculation words
        "Name: Alice Smith, Phone: 1234567890, calculate total of 1234567890",
        
        # Case 5: No direct calculation reference
        "My details: Name is Bob Wilson, Phone is 5555555555, Age is 30",
        
        # Case 6: Complex case with multiple PII
        "I am Sarah Johnson, email sarah@gmail.com, phone 9999999999, tell me addition of 9999999999",
    ]
    
    print("Enhanced Dependency Preservation Test")
    print("=" * 70)
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i}. Input: {test_text}")
        print(f"   Entities: {len(result.entities)}")
        
        preserved_count = 0
        for entity in result.entities:
            if hasattr(entity, 'preserve') and entity.preserve:
                preserved_count += 1
                print(f"   -> PRESERVED: {entity.label}: '{entity.text}'")
            else:
                print(f"   -> ANONYMIZED: {entity.label}: '{entity.text}'")
        
        print(f"   Result: {result.anonymized_text}")
        print(f"   Preserved: {preserved_count}/{len(result.entities)} entities")

if __name__ == "__main__":
    test_enhanced_dependency()
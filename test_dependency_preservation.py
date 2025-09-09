#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_dependency_preservation():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Mathematical dependencies
        "My phone number is 1234567890 and what is the sum of it?",
        "My account number is 9876543210, please calculate the total of 9876543210",
        "The PIN is 1234, what is 1234 + 5678?",
        
        # Direct references
        "My phone is 9876543210, call me at this phone 9876543210",
        "Account: 1234567890, transfer money to account 1234567890",
        "My Aadhaar is 1234 5678 9012, verify this Aadhaar 1234 5678 9012",
        
        # No dependencies (should be anonymized)
        "My phone number is 9876543210 and I live in Mumbai",
        "Contact me at john@gmail.com or call 1234567890",
        
        # Complex case
        "My phone is 9876543210, email is john@gmail.com. What is the sum of 9876543210? Also my address is 123 Main Street."
    ]
    
    print("Dependency Preservation Test")
    print("=" * 60)
    
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
    test_dependency_preservation()
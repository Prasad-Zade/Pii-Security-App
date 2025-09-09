#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_name_variations():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        "my name is prasad zade",
        "I am John Smith",
        "I'm Sarah Johnson", 
        "call me Mike Davis",
        "My name is Raj Patel",
        "i am priya sharma"
    ]
    
    print("Testing Name Detection Variations")
    print("=" * 50)
    
    for test_text in test_cases:
        result = pii_system.process(test_text, include_llm=False)
        entities = [e for e in result.entities if e.label == 'PERSON']
        
        print(f"\nInput: {test_text}")
        if entities:
            print(f"Detected: {entities[0].text} -> {result.anonymized_text}")
        else:
            print("No name detected")

if __name__ == "__main__":
    test_name_variations()
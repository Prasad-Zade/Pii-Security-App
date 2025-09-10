#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_mixed_contexts():
    """Test mixed contexts where some PII should be preserved and some anonymized"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Phone calculation, name anonymized
        ("my name is prasad and my phone number is 1111111111 tell me addition of it", "name anonymized, phone preserved"),
        ("John's phone is 9876543210, calculate sum of it", "name anonymized, phone preserved"),
        
        # Name calculation, phone anonymized  
        ("Count letters in the name Ankit Sharma, my phone is 9876543210", "name preserved, phone anonymized"),
        ("How many characters in John Doe? My number is 1234567890", "name preserved, phone anonymized"),
        
        # Both preserved (both computational)
        ("Add 100 to 9876543210 and count letters in Prasad Zade", "both preserved"),
        
        # Both anonymized (no computation)
        ("My name is Riya and my phone is 9988776655", "both anonymized"),
        
        # Medical + PII
        ("My name is Prasad, I have diabetes, phone: 9876543210", "name anonymized, medical preserved, phone anonymized"),
    ]
    
    print("MIXED CONTEXT SCENARIOS TEST")
    print("=" * 50)
    
    for input_text, expected_behavior in test_cases:
        print(f"\nInput: {input_text}")
        print(f"Expected: {expected_behavior}")
        
        entities = detector.detect_entities(input_text)
        result = anonymizer.anonymize_text(input_text, entities)[0]
        
        print(f"Entities: {[(e.label, e.text, e.preserve) for e in entities]}")
        print(f"Output: {result}")

if __name__ == "__main__":
    test_mixed_contexts()
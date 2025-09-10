#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_simple_assignment_scenarios():
    """Test cases for simple PII assignment that should be anonymized"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Basic assignments
        ("my name is prasad and my phone number is 1111111111", "my name is [NAME] and my phone number is [PHONE]"),
        ("My name is John and my email is john@gmail.com", "My name is [NAME] and my email is [EMAIL]"),
        ("I am Ankit, my phone is 9876543210", "I am [NAME], my phone is [PHONE]"),
        
        # Single assignments
        ("My name is prasad", "My name is [NAME]"),
        ("My phone number is 1111111111", "My phone number is [PHONE]"),
        ("My email is test@gmail.com", "My email is [EMAIL]"),
        ("My address is 123 Main Street", "My address is [ADDRESS]"),
        
        # Different formats
        ("I'm called Riya", "I'm called [NAME]"),
        ("Call me at 9988776655", "Call me at [PHONE]"),
        ("Contact me: 1234567890", "Contact me: [PHONE]"),
        ("Email: admin@company.com", "Email: [EMAIL]"),
        
        # Multiple PII in one sentence
        ("Prasad Zade, phone: 9876543210, email: prasad@gmail.com", "[NAME], phone: [PHONE], email: [EMAIL]"),
        ("John Doe lives at 123 Park Avenue, phone 9988776655", "[NAME] lives at [ADDRESS], phone [PHONE]"),
        
        # Should NOT be anonymized (computational contexts)
        ("Count letters in the name Prasad Zade", "Count letters in the name Prasad Zade"),
        ("Add 1000 to 9876543210", "Add 1000 to 9876543210"),
        ("Check if john@gmail.com contains @ symbol", "Check if john@gmail.com contains @ symbol"),
        ("Validate phone 1234567890 format", "Validate phone 1234567890 format"),
        
        # Medical contexts (preserve medical terms)
        ("My name is Prasad and I have diabetes", "My name is [NAME] and I have diabetes"),
        ("John has cancer, phone: 9876543210", "[NAME] has cancer, phone: [PHONE]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("SIMPLE ASSIGNMENT SCENARIOS TEST")
    print("=" * 50)
    
    for input_text, expected in test_cases:
        entities = detector.detect_entities(input_text)
        result = anonymizer.anonymize_text(input_text, entities)[0]
        
        if result == expected:
            correct += 1
            print(f"PASS: {input_text}")
        else:
            print(f"FAIL: {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
    
    print(f"\nSimple Assignment Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_simple_assignment_scenarios()
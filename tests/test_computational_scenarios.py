#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_computational_scenarios():
    """Test cases for computational context preservation"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Name calculations
        ("Count letters in the name Prasad Zade", "Count letters in the name Prasad Zade"),
        ("How many characters in John Doe", "How many characters in John Doe"),
        ("Length of name Ankit Sharma", "Length of name Ankit Sharma"),
        
        # Phone number calculations
        ("Add 1000 to 7418529632 and tell me the result", "Add 1000 to 7418529632 and tell me the result"),
        ("Multiply 9876543210 by 2", "Multiply 9876543210 by 2"),
        ("What is 1234567890 + 1111111111", "What is 1234567890 + 1111111111"),
        
        # Email calculations
        ("Count characters before @ in prasad123@gmail.com", "Count characters before @ in prasad123@gmail.com"),
        ("Extract domain from john.doe@company.com", "Extract domain from john.doe@company.com"),
        
        # Date calculations
        ("Calculate age from 12-08-1999", "Calculate age from 12-08-1999"),
        ("I was born on 15-05-1995, calculate my age today", "I was born on 15-05-1995, calculate my age today"),
        
        # Credit card validation
        ("Check if 4111 1111 1111 1111 passes the Luhn algorithm", "Check if 4111 1111 1111 1111 passes the Luhn algorithm"),
        ("Validate 5500 0000 0000 0004 using Luhn test", "Validate 5500 0000 0000 0004 using Luhn test"),
        
        # Aadhaar validation
        ("Check if 1234 5678 9101 contains 12 digits", "Check if 1234 5678 9101 contains 12 digits"),
        ("Verify Aadhaar 9876 5432 1098 format", "Verify Aadhaar 9876 5432 1098 format"),
        
        # PAN validation
        ("Check if ABCDE1234F follows correct PAN format", "Check if ABCDE1234F follows correct PAN format"),
        ("Validate PAN XYZZZ9999Z structure", "Validate PAN XYZZZ9999Z structure"),
        
        # IP address validation
        ("Check if 192.168.1.1 is a private IP range", "Check if 192.168.1.1 is a private IP range"),
        ("Is 8.8.8.8 a public IP address", "Is 8.8.8.8 a public IP address"),
        
        # Vehicle number validation
        ("Check if MH12AB1234 has 10 characters", "Check if MH12AB1234 has 10 characters"),
        ("Validate vehicle number DL8CAF5031 format", "Validate vehicle number DL8CAF5031 format"),
        
        # Distance calculations
        ("Find distance between 123 Shivaji Nagar, Pune and Mumbai", "Find distance between 123 Shivaji Nagar, Pune and Mumbai"),
        
        # Non-computational (should anonymize)
        ("My name is Prasad Zade", "My name is [NAME]"),
        ("Please save my number 9876543210", "Please save my number [PHONE]"),
        ("Send email to john@gmail.com", "Send email to [EMAIL]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("COMPUTATIONAL SCENARIOS TEST")
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
    
    print(f"\nComputational Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_computational_scenarios()
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_medical_conditions():
    """Test medical condition preservation"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        ("My name is Prasad Zade and I have diabetes tell me what to eat", "[NAME] and I have diabetes tell me what to eat"),
        ("John has cancer and needs treatment", "[NAME] has cancer and needs treatment"),
        ("I suffer from hypertension", "I suffer from hypertension"),
        ("My phone is 9876543210 and I have asthma", "My phone is [PHONE] and I have asthma"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    for input_text, expected in test_cases:
        entities = detector.detect_entities(input_text)
        result = anonymizer.anonymize_text(input_text, entities)[0]
        if expected in result:
            correct += 1
            print(f"PASS: {input_text}")
        else:
            print(f"FAIL: {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
    
    return correct, total

def test_computational_preservation():
    """Test computational context preservation"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        ("Count letters in the name Prasad Zade", "Count letters in the name Prasad Zade"),
        ("Add 1000 to 7418529632 and tell me the result", "Add 1000 to 7418529632 and tell me the result"),
        ("Check if 4111 1111 1111 1111 passes the Luhn algorithm", "Check if 4111 1111 1111 1111 passes the Luhn algorithm"),
        ("My name is Prasad Zade", "My name is [NAME]"),
        ("Please save my number 9876543210", "Please save my number [PHONE]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    for input_text, expected in test_cases:
        entities = detector.detect_entities(input_text)
        result = anonymizer.anonymize_text(input_text, entities)[0]
        if expected == result:
            correct += 1
            print(f"PASS: {input_text}")
        else:
            print(f"FAIL: {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
    
    return correct, total

def test_pii_detection():
    """Test basic PII detection"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        ("My email is prasad123@gmail.com", "My email is [EMAIL]"),
        ("Call me at 9876543210", "Call me at [PHONE]"),
        ("I live at 123 Shivaji Nagar, Pune", "I live at [ADDRESS]"),
        ("My Aadhaar is 1234 5678 9101", "My Aadhaar is [AADHAAR]"),
        ("PAN number is ABCDE1234F", "PAN number is [PAN]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    for input_text, expected in test_cases:
        entities = detector.detect_entities(input_text)
        result = anonymizer.anonymize_text(input_text, entities)[0]
        if expected == result:
            correct += 1
            print(f"PASS: {input_text}")
        else:
            print(f"FAIL: {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
    
    return correct, total

def main():
    print("=" * 60)
    print("PII PRIVACY PROTECTION SYSTEM - ACCURACY TEST")
    print("=" * 60)
    
    total_correct = 0
    total_tests = 0
    
    print("\n1. Testing Medical Condition Preservation...")
    print("-" * 40)
    correct, tests = test_medical_conditions()
    total_correct += correct
    total_tests += tests
    print(f"Medical Tests: {correct}/{tests} ({correct/tests*100:.1f}%)")
    
    print("\n2. Testing Computational Context Preservation...")
    print("-" * 40)
    correct, tests = test_computational_preservation()
    total_correct += correct
    total_tests += tests
    print(f"Computational Tests: {correct}/{tests} ({correct/tests*100:.1f}%)")
    
    print("\n3. Testing Basic PII Detection...")
    print("-" * 40)
    correct, tests = test_pii_detection()
    total_correct += correct
    total_tests += tests
    print(f"PII Detection Tests: {correct}/{tests} ({correct/tests*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print(f"OVERALL ACCURACY: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print("=" * 60)
    
    return total_correct/total_tests*100

if __name__ == "__main__":
    main()
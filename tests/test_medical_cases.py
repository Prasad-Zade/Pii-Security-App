#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_medical_cases():
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        ("My name is Prasad Zade and I have Diabetes.", "My name is [NAME] and I have Diabetes."),
        ("I am Ankit Sharma, recently diagnosed with Hypertension.", "I am [NAME], recently diagnosed with Hypertension."),
        ("My name is Riya Mehta and I am suffering from Asthma.", "My name is [NAME] and I am suffering from Asthma."),
        ("This is John Doe, I have been treated for Cancer.", "This is [NAME], I have been treated for Cancer."),
        ("My name is Neha Patil and I have a history of Migraine.", "My name is [NAME] and I have a history of Migraine."),
        ("I am Suresh Kumar, diagnosed with Tuberculosis last month.", "I am [NAME], diagnosed with Tuberculosis last month."),
        ("My name is Arjun Reddy and I take insulin for Type 1 Diabetes.", "My name is [NAME] and I take insulin for Type 1 Diabetes."),
        ("my name is Prasad Zade and I have Dibaties", "my name is [NAME] and I have Dibaties"),
    ]
    
    correct = 0
    total = len(test_cases)
    
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
            print(f"  Entities: {[(e.label, e.text, e.preserve) for e in entities]}")
    
    print(f"\nAccuracy: {correct}/{total} ({correct/total*100:.1f}%)")

if __name__ == "__main__":
    test_medical_cases()
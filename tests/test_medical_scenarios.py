#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_medical_scenarios():
    """Comprehensive medical condition test cases"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Basic medical conditions with names
        ("My name is Prasad Zade and I have Diabetes.", "My name is [NAME] and I have Diabetes."),
        ("I am Ankit Sharma, recently diagnosed with Hypertension.", "I am [NAME], recently diagnosed with Hypertension."),
        ("My name is Riya Mehta and I am suffering from Asthma.", "My name is [NAME] and I am suffering from Asthma."),
        ("This is John Doe, I have been treated for Cancer.", "This is [NAME], I have been treated for Cancer."),
        ("My name is Neha Patil and I have a history of Migraine.", "My name is [NAME] and I have a history of Migraine."),
        ("I am Suresh Kumar, diagnosed with Tuberculosis last month.", "I am [NAME], diagnosed with Tuberculosis last month."),
        ("My name is Arjun Reddy and I take insulin for Type 1 Diabetes.", "My name is [NAME] and I take insulin for Type 1 Diabetes."),
        
        # Medical misspellings
        ("my name is Prasad Zade and I have Dibaties", "my name is [NAME] and I have Dibaties"),
        ("John has cancor and needs help", "[NAME] has cancor and needs help"),
        ("I suffer from astma since childhood", "I suffer from astma since childhood"),
        
        # Medical advice requests
        ("My name is Prasad Zade and I have diabetes tell me what to eat", "My name is [NAME] and I have diabetes tell me what to eat"),
        ("I have hypertension, suggest diet plan", "I have hypertension, suggest diet plan"),
        ("Suffering from migraine, what medicine to take", "Suffering from migraine, what medicine to take"),
        
        # Medical with contact info
        ("My phone is 9876543210 and I have asthma", "My phone is [PHONE] and I have asthma"),
        ("Email me at john@gmail.com about my diabetes treatment", "Email me at [EMAIL] about my diabetes treatment"),
        
        # Complex medical scenarios
        ("Patient Rahul Sharma, age 45, diagnosed with heart disease", "Patient [NAME], age [AGE], diagnosed with heart disease"),
        ("Mrs. Priya Patel has been suffering from arthritis for 5 years", "Mrs. [NAME] has been suffering from arthritis for 5 years"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("MEDICAL SCENARIOS TEST")
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
    
    print(f"\nMedical Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_medical_scenarios()
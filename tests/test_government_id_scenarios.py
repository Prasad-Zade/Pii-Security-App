#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_government_id_scenarios():
    """Test cases for government IDs (Aadhaar, PAN, Passport, etc.)"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Aadhaar numbers
        ("My Aadhaar number is 1234 5678 9101", "My Aadhaar number is [AADHAAR]"),
        ("Aadhaar: 9876-5432-1098", "Aadhaar: [AADHAAR]"),
        ("Submit Aadhaar 5555666677778888", "Submit Aadhaar [AADHAAR]"),
        
        # PAN numbers
        ("My PAN is ABCDE1234F", "My PAN is [PAN]"),
        ("PAN number: XYZZZ9999Z", "PAN number: [PAN]"),
        ("Tax ID PQRST5678U for filing", "Tax ID [PAN] for filing"),
        
        # Passport numbers
        ("My passport number is Z1234567", "My passport number is [PASSPORT]"),
        ("Passport: M9876543 for US visa", "Passport: [PASSPORT] for US visa"),
        ("Travel document A1122334", "Travel document [PASSPORT]"),
        
        # SSN (for international users)
        ("My SSN is 987-65-4320", "My SSN is [SSN]"),
        ("Social Security: 123456789", "Social Security: [SSN]"),
        
        # Driving License
        ("License number: MH1234567890123", "License number: [DRIVING_LICENSE]"),
        ("DL: KA9876543210987", "DL: [DRIVING_LICENSE]"),
        
        # Voter ID
        ("Voter ID: ABC1234567", "Voter ID: [VOTER_ID]"),
        ("Election card XYZ9876543", "Election card [VOTER_ID]"),
        
        # Employee/Student IDs
        ("Employee ID: EMP12345", "Employee ID: [EMPLOYEE_ID]"),
        ("Staff number: STAFF9876", "Staff number: [EMPLOYEE_ID]"),
        ("Student ID: STU555666", "Student ID: [STUDENT_ID]"),
        ("Roll number: ROLL123456", "Roll number: [STUDENT_ID]"),
        
        # Mixed scenarios with names
        ("Prasad Zade's Aadhaar is 1234 5678 9101", "[NAME]'s Aadhaar is [AADHAAR]"),
        ("John Doe, PAN: ABCDE1234F, Passport: Z1234567", "[NAME], PAN: [PAN], Passport: [PASSPORT]"),
        ("Ankit Sharma applied with Aadhaar 9876543210123", "[NAME] applied with Aadhaar [AADHAAR]"),
        
        # Validation scenarios (should preserve for computation)
        ("Check if 1234 5678 9101 contains 12 digits", "Check if 1234 5678 9101 contains 12 digits"),
        ("Validate PAN ABCDE1234F format", "Validate PAN ABCDE1234F format"),
        ("Verify passport Z1234567 has 8 characters", "Verify passport Z1234567 has 8 characters"),
        
        # Vehicle numbers
        ("My car number is MH12AB1234", "My car number is [VEHICLE]"),
        ("Vehicle: DL8CAF5031", "Vehicle: [VEHICLE]"),
        ("Bike registration KA01BC9999", "Bike registration [VEHICLE]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("GOVERNMENT ID SCENARIOS TEST")
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
    
    print(f"\nGovernment ID Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_government_id_scenarios()
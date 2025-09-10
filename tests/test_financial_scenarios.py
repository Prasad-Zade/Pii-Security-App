#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_financial_scenarios():
    """Comprehensive financial PII test cases"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Bank accounts
        ("My account number is 123456789012", "My account number is [BANK_ACC]"),
        ("Transfer money to account 987654321098", "Transfer money to account [BANK_ACC]"),
        ("Prasad Zade's account is 555666777888", "[NAME]'s account is [BANK_ACC]"),
        
        # Credit cards
        ("My card number is 4111 1111 1111 1111", "My card number is [CREDIT_CARD]"),
        ("Use card 5500 0000 0000 0004 for payment", "Use card [CREDIT_CARD] for payment"),
        ("John paid with 4000123456789010", "[NAME] paid with [CREDIT_CARD]"),
        
        # Credit card calculations (should preserve)
        ("Check if 4111 1111 1111 1111 passes the Luhn algorithm", "Check if 4111 1111 1111 1111 passes the Luhn algorithm"),
        ("Validate card 5500 0000 0000 0004 using Luhn", "Validate card 5500 0000 0000 0004 using Luhn"),
        
        # PAN numbers
        ("My PAN is ABCDE1234F", "My PAN is [PAN]"),
        ("PAN number XYZZZ9999Z belongs to Ankit", "PAN number [PAN] belongs to [NAME]"),
        ("Check if ABCDE1234F follows correct PAN format", "Check if ABCDE1234F follows correct PAN format"),
        
        # UPI and digital payments
        ("My UPI ID is prasad@paytm", "My UPI ID is [UPI_ID]"),
        ("Send money to john.doe@gpay", "Send money to [UPI_ID]"),
        
        # Salary information
        ("My salary is Rs.50000 per month", "My salary is [SALARY] per month"),
        ("Annual income: $75000", "Annual income: [SALARY]"),
        
        # Mixed financial scenarios
        ("Prasad Zade, PAN: ABCDE1234F, Account: 123456789012", "[NAME], PAN: [PAN], Account: [BANK_ACC]"),
        ("Transfer Rs.10000 from 111222333444 to 555666777888", "Transfer Rs.10000 from [BANK_ACC] to [BANK_ACC]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("FINANCIAL SCENARIOS TEST")
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
    
    print(f"\nFinancial Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_financial_scenarios()
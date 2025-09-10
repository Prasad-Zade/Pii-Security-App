#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_all_pii_cases():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # 1. Name
        ("My name is Prasad Zade.", "MASK ALL"),
        ("My name is Prasad Zade and count letters in my name.", "PRESERVE name"),
        
        # 2. Phone Number
        ("My phone number is 1478523697.", "MASK ALL"),
        ("My phone number is 7418529632, add 5 to it.", "PRESERVE phone"),
        
        # 3. Email
        ("Contact me at prasad123@gmail.com.", "MASK ALL"),
        ("My email is prasad123@gmail.com, tell me its domain.", "PRESERVE email"),
        
        # 4. Date of Birth
        ("My date of birth is 12-08-1999.", "MASK ALL"),
        ("I was born on 12-08-1999, calculate my age.", "PRESERVE date"),
        
        # 5. Address
        ("I live at 123 Shivaji Nagar, Pune.", "MASK ALL"),
        ("Distance from 123 Shivaji Nagar, Pune to Mumbai?", "PRESERVE address"),
        
        # 6. Aadhaar
        ("My Aadhaar number is 1234 5678 9101.", "MASK ALL"),
        ("Sum digits of 1234 5678 9101.", "PRESERVE aadhaar"),
        
        # 7. Passport
        ("My passport number is Z1234567.", "MASK ALL"),
        ("Check if Z1234567 has 8 characters.", "PRESERVE passport"),
        
        # 8. PAN
        ("My PAN is ABCDE1234F.", "MASK ALL"),
        ("Check if ABCDE1234F matches PAN format.", "PRESERVE pan"),
        
        # 9. Bank Account
        ("My account number is 123456789012.", "MASK ALL"),
        ("Multiply my account number 123456789012 by 2.", "PRESERVE account"),
        
        # 10. Credit Card
        ("My credit card number is 4111 1111 1111 1111.", "MASK ALL"),
        ("Check if 4111 1111 1111 1111 is valid card using Luhn algorithm.", "PRESERVE card"),
        
        # 11. IP Address
        ("My IP is 192.168.0.1.", "MASK ALL"),
        ("Check if 192.168.0.1 belongs to private IP range.", "PRESERVE ip"),
        
        # 12. Vehicle Number
        ("My car number is MH12AB1234.", "MASK ALL"),
        ("Check if MH12AB1234 is a valid vehicle number format.", "PRESERVE vehicle"),
        
        # 13. Medical Record
        ("My hospital patient ID is HOSP123456.", "MASK ALL"),
        ("Count characters in HOSP123456.", "PRESERVE medical_id"),
    ]
    
    print("Comprehensive PII Test Cases")
    print("=" * 80)
    
    for i, (test_text, expected) in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i:2d}. {expected}")
        print(f"    Input: {test_text}")
        print(f"    Entities: {len(result.entities)}")
        
        preserved_count = 0
        masked_count = 0
        
        for entity in result.entities:
            if hasattr(entity, 'preserve') and entity.preserve:
                preserved_count += 1
                print(f"    -> PRESERVED: {entity.label}: '{entity.text}' (needed for task)")
            else:
                masked_count += 1
                print(f"    -> MASKED: {entity.label}: '{entity.text}' -> FAKE DATA")
        
        print(f"    Result: {result.anonymized_text}")
        
        # Check if behavior matches expectation
        if "PRESERVE" in expected and preserved_count > 0:
            print(f"    [OK] CORRECT: Preserved {preserved_count} entities as expected")
        elif "MASK ALL" in expected and preserved_count == 0:
            print(f"    [OK] CORRECT: Masked all {masked_count} entities as expected")
        else:
            print(f"    [ERROR] INCORRECT: Expected {expected}, got {preserved_count} preserved, {masked_count} masked")

if __name__ == "__main__":
    test_all_pii_cases()
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_comprehensive_scenarios():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Names
        ("My name is Prasad Zade and I booked flight tickets.", "MASK", "name not needed for task"),
        ("Check if the name Prasad Zade has more than 10 letters.", "PRESERVE", "name needed for counting"),
        ("Prasad Zade sent 5000 to Ankit Sharma.", "MASK", "names not needed"),
        
        # Phone Numbers
        ("Please call me at 9876543210 after 6 PM.", "MASK", "phone not needed"),
        ("Check if 9876543210 is divisible by 2.", "PRESERVE", "phone needed for math"),
        ("I transferred money from 7418529632 to 9632587410.", "MASK", "phones not needed"),
        
        # Emails
        ("My email is prasad123@gmail.com for job updates.", "MASK", "email not needed"),
        ("Count letters before @ in prasad123@gmail.com.", "PRESERVE", "email needed for counting"),
        ("Forward CV from prasad123@gmail.com to hr@company.com.", "MASK", "emails not needed"),
        
        # Dates
        ("My DOB is 12/08/1999.", "MASK", "date not needed"),
        ("I was born on 12/08/1999, calculate my current age.", "PRESERVE", "date needed for age calc"),
        ("Prasad Zade, born on 12/08/1999, applied for PAN.", "MASK", "date not needed"),
        
        # Addresses
        ("I live at 123 Shivaji Nagar, Pune.", "MASK", "address not needed"),
        ("Find the distance between 123 Shivaji Nagar, Pune and Mumbai.", "PRESERVE", "address needed for distance"),
        ("Deliver parcel to 45 MG Road, Delhi for Ankit.", "MASK", "address not needed"),
        
        # Aadhaar
        ("My Aadhaar is 1234 5678 9101.", "MASK", "aadhaar not needed"),
        ("Check if Aadhaar 1234 5678 9101 has 12 digits.", "PRESERVE", "aadhaar needed for counting"),
        ("John's SSN is 987-65-4320 and DOB is 12-08-1999.", "MASK", "ssn/dob not needed"),
        
        # Passport
        ("Passport number Z1234567 is valid.", "MASK", "passport not needed"),
        ("Check if Z1234567 has 8 characters.", "PRESERVE", "passport needed for counting"),
        ("Prasad Zade with passport M9876543 applied for a visa.", "MASK", "passport not needed"),
        
        # PAN
        ("My PAN number is ABCDE1234F.", "MASK", "pan not needed"),
        ("Check if ABCDE1234F follows PAN format.", "PRESERVE", "pan needed for validation"),
        ("PAN XYZZZ9999Z belongs to Ankit Sharma.", "MASK", "pan not needed"),
        
        # Bank Account
        ("My account number is 123456789012.", "MASK", "account not needed"),
        ("Add 2000 to account number 123456789012.", "PRESERVE", "account needed for math"),
        ("Transfer from 123456789012 to 987654321098 by Ankit.", "MASK", "accounts not needed"),
        
        # Credit Card
        ("Card number 4111 1111 1111 1111 is mine.", "MASK", "card not needed"),
        ("Check if 4111 1111 1111 1111 passes Luhn algorithm.", "PRESERVE", "card needed for validation"),
        ("Prasad used 5500 0000 0000 0004 for shopping.", "MASK", "card not needed"),
        
        # IP Address
        ("Server IP is 192.168.1.1.", "MASK", "ip not needed"),
        ("Check if 192.168.1.1 is a private IP address.", "PRESERVE", "ip needed for validation"),
        ("User Ankit logged in from 8.8.8.8.", "MASK", "ip not needed"),
        
        # Vehicle Number
        ("Car number MH12AB1234 is parked outside.", "MASK", "vehicle not needed"),
        ("Check if MH12AB1234 has 10 characters.", "PRESERVE", "vehicle needed for counting"),
        ("Ankit drives DL8CAF5031 to office.", "MASK", "vehicle not needed"),
        
        # Medical ID
        ("My hospital record is HOSP123456.", "MASK", "medical id not needed"),
        ("Count characters in HOSP123456.", "PRESERVE", "medical id needed for counting"),
        ("Patient Prasad with ID MED999888 admitted.", "MASK", "medical id not needed"),
    ]
    
    print("Comprehensive PII Scenario Testing")
    print("=" * 80)
    
    correct = 0
    total = len(test_cases)
    
    for i, (test_text, expected_behavior, reason) in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i:2d}. {test_text}")
        print(f"    Expected: {expected_behavior} ({reason})")
        
        preserved_count = 0
        masked_count = 0
        
        for entity in result.entities:
            if hasattr(entity, 'preserve') and entity.preserve:
                preserved_count += 1
                print(f"    -> PRESERVED: {entity.label}: '{entity.text}'")
            else:
                masked_count += 1
                print(f"    -> MASKED: {entity.label}: '{entity.text}'")
        
        print(f"    Result: {result.anonymized_text}")
        
        # Check correctness
        if expected_behavior == "PRESERVE" and preserved_count > 0:
            print(f"    [OK] Correctly preserved {preserved_count} entities")
            correct += 1
        elif expected_behavior == "MASK" and preserved_count == 0:
            print(f"    [OK] Correctly masked all {masked_count} entities")
            correct += 1
        else:
            print(f"    [ERROR] Expected {expected_behavior}, got {preserved_count} preserved, {masked_count} masked")
    
    print(f"\n" + "=" * 80)
    print(f"FINAL SCORE: {correct}/{total} ({correct/total*100:.1f}%) test cases passed")
    print("=" * 80)

if __name__ == "__main__":
    test_comprehensive_scenarios()
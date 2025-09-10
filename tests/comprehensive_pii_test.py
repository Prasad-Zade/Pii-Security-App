#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_all_pii_types():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Names
        "My name is Rajesh Kumar",
        "I am Priya Sharma",
        
        # Phone numbers
        "Call me at 9876543210",
        "My number is +91 98765 43210",
        "Phone: (555) 123-4567",
        
        # Aadhaar numbers
        "My Aadhaar is 1234 5678 9012",
        "Aadhaar: 2345-6789-0123",
        
        # PAN cards
        "PAN number: ABCDE1234F",
        "My PAN is XYZAB5678C",
        
        # Passport
        "Passport: A1234567",
        "My passport number is AB123456",
        
        # Driving License
        "DL: MH1234567890123",
        "License number: KA12345678",
        
        # Voter ID
        "Voter ID: ABC1234567",
        
        # Bank details
        "Account number: 123456789012",
        "IFSC: SBIN0001234",
        
        # Credit card
        "Card: 4532 1234 5678 9012",
        "CVV: 123",
        "PIN: 1234",
        
        # Email
        "Email: john.doe@gmail.com",
        "Contact: user@company.co.in",
        
        # Age
        "I am 25 years old",
        "Age: 30",
        "Aged 45",
        
        # Address
        "Address: 123 Main Street, Mumbai",
        "Live at 456 Park Avenue",
        
        # Medical
        "Medical record: MRN123456",
        "Patient has diabetes",
        
        # Employee/Student ID
        "Employee ID: EMP12345",
        "Student roll: STU67890",
        
        # Dates
        "DOB: 15/08/1990",
        "Born on 1990-08-15",
        
        # IP Address
        "Server IP: 192.168.1.100",
        
        # SSN (US)
        "SSN: 123-45-6789",
        
        # Complex mixed case
        "Hi, I'm Amit Patel, age 28, phone 9876543210, email amit@gmail.com, Aadhaar 1234-5678-9012, living at 123 MG Road, Bangalore"
    ]
    
    print("Comprehensive PII Detection Test")
    print("=" * 80)
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i:2d}. Input: {test_text}")
        print(f"    Entities found: {len(result.entities)}")
        
        for entity in result.entities:
            print(f"    -> {entity.label}: '{entity.text}'")
        
        print(f"    Result: {result.anonymized_text}")
        print(f"    Privacy Score: {result.privacy_score}%")

if __name__ == "__main__":
    test_all_pii_types()
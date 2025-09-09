#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_ultimate_pii():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Basic Identity
        "My name is Rajesh Kumar, I am male, age: 28, nationality: Indian, religion: Hindu",
        "Father's name: Suresh Patel, Mother's name: Priya Patel",
        "DOB: 15/08/1995, born on 1995-08-15",
        
        # Contact Information  
        "Email: rajesh@gmail.com, Phone: 9876543210, Address: 123 MG Road, Bangalore",
        "PIN: 560001, Social: @rajesh_kumar, twitter.com/rajesh123",
        
        # Government IDs
        "Aadhaar: 1234 5678 9012, PAN: ABCDE1234F, Passport: A1234567",
        "Voter ID: ABC1234567, Driving License: KA1234567890123",
        "Employee ID: EMP12345, Student roll: STU67890",
        "SSN: 123-45-6789",
        
        # Financial Information
        "Account: 123456789012, IFSC: SBIN0001234, UPI: rajesh@paytm",
        "Credit Card: 4532 1234 5678 9012, CVV: 123",
        "Salary: Rs.500000, Income: $50000",
        
        # Health & Biometric
        "Blood group: B+, Medical record: MRN123456",
        "Patient has diabetes and hypertension",
        
        # Travel & Transport
        "Vehicle: KA01AB1234",
        
        # Digital Identifiers
        "IP: 192.168.1.100, MAC: 00:1B:44:11:3A:B7, IMEI: 123456789012345",
        
        # Complex mixed case
        "Hi, I'm Amit Sharma, male, age: 30, email: amit@company.com, phone: +91-9876543210, Aadhaar: 2345-6789-0123, PAN: XYZAB1234C, address: 456 Park Street, Mumbai, PIN: 400001, blood group: A+, vehicle: MH01CD5678, salary: Rs.800000"
    ]
    
    print("Ultimate PII Detection Test - All Categories")
    print("=" * 80)
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i:2d}. Input: {test_text}")
        print(f"    Entities: {len(result.entities)}")
        
        for entity in result.entities:
            print(f"    -> {entity.label}: '{entity.text}'")
        
        print(f"    Result: {result.anonymized_text}")
        print(f"    Privacy Score: {result.privacy_score}%")

if __name__ == "__main__":
    test_ultimate_pii()
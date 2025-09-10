#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_enhanced_pii_detection():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Complete personal profile
        "Full Name: Rajesh Kumar Sharma, Father's Name: Suresh Kumar, DOB: 15/08/1990, Age: 33, Gender: Male, Religion: Hindu, Caste: OBC",
        
        # Contact details
        "Phone: +91-9876543210, Email: rajesh.sharma@gmail.com, Address: 123 MG Road, Bangalore, PIN: 560001",
        
        # Government IDs
        "Aadhaar: 1234 5678 9012, PAN: ABCDE1234F, Passport: A1234567, Voter ID: XYZ1234567, Driving License: KA1234567890123",
        
        # Financial information
        "Bank Account: 123456789012, IFSC: HDFC0001234, Credit Card: 4532 1234 5678 9012, CVV: 123, UPI: rajesh@paytm, Salary: Rs. 800000",
        
        # Professional details
        "Occupation: Software Engineer, Employer: Infosys Technologies, Employee ID: INF12345, Experience: 8 years",
        
        # Academic information
        "University: Bangalore University, Degree: B.Tech Computer Science, CGPA: 8.5",
        
        # Health information
        "Blood Group: B+, Height: 5'9\", Weight: 70kg, Patient ID: HOSP1234",
        
        # Travel information
        "Vehicle Number: KA01AB1234, Flight Booking: AI123456789",
        
        # Digital identifiers
        "IP Address: 192.168.1.100, MAC Address: 00:1A:2B:3C:4D:5E, IMEI: 356938035643809",
        
        # Location information
        "Current Location: Bangalore Karnataka, Hometown: Mysore",
        
        # Sensitive information
        "Political Party: XYZ Party, Criminal Case: FIR123456",
        
        # Mixed case with calculation (should preserve only calculation-referenced data)
        "My name is John Doe, phone 9999999999, salary 500000, tell me addition of 9999999999",
    ]
    
    print("Enhanced PII Detection Test")
    print("=" * 80)
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"\n{i:2d}. Input: {test_text}")
        print(f"    Entities detected: {len(result.entities)}")
        
        for entity in result.entities:
            status = "PRESERVED" if (hasattr(entity, 'preserve') and entity.preserve) else "ANONYMIZED"
            print(f"    -> {status}: {entity.label}: '{entity.text}'")
        
        print(f"    Result: {result.anonymized_text}")
        print(f"    Privacy Score: {result.privacy_score}%")

if __name__ == "__main__":
    test_enhanced_pii_detection()
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_comprehensive_pii_protection():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # 1. Basic Identity - Should ALL be anonymized unless in calculation
        "My name is John Smith and I am 28 years old",
        "DOB: 12/09/1999, Nationality: Indian, Gender: Male",
        "Title: Dr. Rajesh Gupta, Marital Status: Married",
        
        # 2. Family & Relationships - Should ALL be anonymized
        "Father's name is Robert Smith, Mother: Mary Johnson",
        "Spouse: Priya Ramesh, Children: Arjun and Kavya",
        
        # 3. Contact Information - Should ALL be anonymized unless in calculation
        "Call me at +91 9876543210, Email: john.smith@gmail.com",
        "Address: 123 Main Street, Pune, Maharashtra, 411001",
        "LinkedIn: linkedin.com/in/john-smith, Twitter: @johnsmith",
        
        # 4. Government & Legal IDs - Should ALL be anonymized unless in calculation
        "Aadhaar: 1234 5678 9876, PAN: ABCDE1234F",
        "Passport No: M1234567, Voter ID: XYZ1234567",
        "Driving License: MH12AB1234, SSN: 123-45-6789",
        
        # 5. Financial Information - Should ALL be anonymized unless in calculation
        "Bank A/C: 123456789012, IFSC: HDFC0001234",
        "Credit Card: 4111 1111 1111 1111, CVV: 123",
        "UPI ID: john@paytm, Salary: 900000 INR per annum",
        
        # 6. Professional Details - Should ALL be anonymized
        "I work as Software Engineer at Infosys, Employee ID: INF12345",
        "Experience: 5 years at TCS, Department: IT Services",
        
        # 7. Academic Information - Should ALL be anonymized
        "I studied at Zeal College Pune, Roll No: TE12345",
        "Degree: B.Tech Computer Science, CGPA: 8.5",
        
        # 8. Health & Biometric - Should ALL be anonymized
        "Blood Group: B+, Height: 5'9, Weight: 70kg",
        "Patient ID: HOSP1234, Medical Record: MR567890",
        
        # 9. Travel & Transport - Should ALL be anonymized
        "Vehicle Number: MH12AB1234, Flight Booking: AI123456789",
        "Frequent Flyer ID: FF12345",
        
        # 10. Utility & Subscriptions - Should ALL be anonymized
        "Electricity Bill: EB1234567, Netflix ID: user123@netflix.com",
        
        # 11. Digital Identifiers - Should ALL be anonymized
        "IP: 192.168.1.1, MAC: 00:1A:2B:3C:4D:5E",
        "IMEI: 356938035643809, AWS Account: 1234-5678-9012",
        
        # 12. Location - Should ALL be anonymized
        "Current location: Pune Maharashtra, Hometown: Nagpur",
        
        # 13. Sensitive & Cultural - Should ALL be anonymized
        "Caste: OBC, Religion: Hindu, Political: XYZ Party",
        
        # CALCULATION CASES - Only referenced data should be preserved
        "My phone is 9876543210, tell me sum of 9876543210",
        "Account number 1234567890, calculate total of 1234567890",
        "Name: Alice, Phone: 5555555555, what is 5555555555 + 1111111111?",
        
        # MIXED CASES - Only calculation-referenced data preserved
        "I am John Doe, phone 9999999999, email john@gmail.com, tell me addition of 9999999999",
        "Name: Sarah, Age: 25, Salary: 500000, calculate 500000 * 12",
        
        # NO CALCULATION - Everything should be anonymized
        "Personal details: Name is Bob Wilson, Phone: 8888888888, Address: 123 Oak Street"
    ]
    
    print("Comprehensive PII Protection Test")
    print("=" * 80)
    print("[RULE] Should anonymize ALL PII unless specifically referenced in calculations")
    print()
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        
        print(f"{i:2d}. Input: {test_text}")
        print(f"    Entities: {len(result.entities)}")
        
        preserved_count = 0
        anonymized_count = 0
        
        for entity in result.entities:
            if hasattr(entity, 'preserve') and entity.preserve:
                preserved_count += 1
                print(f"    -> PRESERVED: {entity.label}: '{entity.text}' (calculation reference)")
            else:
                anonymized_count += 1
                print(f"    -> ANONYMIZED: {entity.label}: '{entity.text}'")
        
        print(f"    Result: {result.anonymized_text}")
        print(f"    Privacy: {anonymized_count} anonymized, {preserved_count} preserved")
        print(f"    Score: {result.privacy_score}%")
        print()

if __name__ == "__main__":
    test_comprehensive_pii_protection()
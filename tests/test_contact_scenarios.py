#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.comprehensive_detector import ComprehensivePIIDetector
from src.core.comprehensive_anonymizer import ComprehensiveAnonymizer

def test_contact_scenarios():
    """Test cases for contact information (phone, email, address)"""
    detector = ComprehensivePIIDetector()
    anonymizer = ComprehensiveAnonymizer()
    
    test_cases = [
        # Phone numbers
        ("My phone number is 9876543210", "My phone number is [PHONE]"),
        ("Call me at +91-9876543210", "Call me at [PHONE]"),
        ("Contact: 022-12345678", "Contact: [PHONE]"),
        ("Please save number 9632587410", "Please save number [PHONE]"),
        ("Send OTP to 7418529632", "Send OTP to [PHONE]"),
        
        # Email addresses
        ("My email is prasad123@gmail.com", "My email is [EMAIL]"),
        ("Contact me at john.doe@company.com", "Contact me at [EMAIL]"),
        ("Send report to admin@website.org", "Send report to [EMAIL]"),
        ("Forward CV to hr@company.com", "Forward CV to [EMAIL]"),
        
        # Addresses
        ("I live at 123 Shivaji Nagar, Pune", "I live at [ADDRESS]"),
        ("Deliver to 45 MG Road, Delhi", "Deliver to [ADDRESS]"),
        ("Office address: 789 Park Street, Mumbai", "Office address: [ADDRESS]"),
        ("Ship to 321 Gandhi Colony, Bangalore", "Ship to [ADDRESS]"),
        
        # Mixed contact scenarios
        ("Prasad Zade, Phone: 9876543210, Email: prasad@gmail.com", "[NAME], Phone: [PHONE], Email: [EMAIL]"),
        ("Contact John at 9988776655 or john@company.com", "Contact [NAME] at [PHONE] or [EMAIL]"),
        ("Ankit Sharma lives at 123 Main Street, call 9876543210", "[NAME] lives at [ADDRESS], call [PHONE]"),
        
        # Social media
        ("Follow me @john_doe on Twitter", "Follow me [SOCIAL_MEDIA] on Twitter"),
        ("Check my profile: linkedin.com/in/prasad", "Check my profile: [SOCIAL_MEDIA]"),
        
        # PIN codes
        ("My area PIN code is 411001", "My area [PIN_CODE]"),
        ("Postal code: 560001 for Bangalore", "[PIN_CODE] for Bangalore"),
        
        # Contact with names
        ("Save Prasad's number 9876543210 in contacts", "Save [NAME]'s number [PHONE] in contacts"),
        ("Email Ankit at ankit@gmail.com about meeting", "Email [NAME] at [EMAIL] about meeting"),
        ("Visit Riya at 123 Park Avenue, Mumbai", "Visit [NAME] at [ADDRESS]"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("CONTACT SCENARIOS TEST")
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
    
    print(f"\nContact Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    return correct, total

if __name__ == "__main__":
    test_contact_scenarios()
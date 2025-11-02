# -*- coding: utf-8 -*-
"""
Test script for Faker-based PII masking
"""

from faker_masking import FakerMasking


def test_faker_masking():
    """Test the FakerMasking utility"""
    
    masker = FakerMasking()
    
    # Test cases
    test_cases = [
        "My email is john@example.com and phone is 9876543210",
        "My name is John Doe and my Aadhaar is 123456789012",
        "Contact me at alice@test.com or call 5551234567",
        "My PAN is ABCDE1234F and SSN is 123-45-6789",
    ]
    
    print("=" * 80)
    print("FAKER-BASED PII MASKING TEST")
    print("=" * 80)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original: {text}")
        
        masked, replacements, detected = masker.mask_text(text)
        
        print(f"Masked:   {masked}")
        print(f"Detected: {', '.join(detected)}")
        print(f"Replacements: {len(replacements)} items")
        
        # Test unmask
        unmasked = masker.unmask_text(masked, replacements)
        print(f"Unmasked: {unmasked}")
        print(f"Match: {'PASS' if unmasked == text else 'FAIL'}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    test_faker_masking()

#!/usr/bin/env python3

from src.core.pii_system import PIIPrivacySystem
from src.core.enhanced_detector import EnhancedPIIDetector

def test_lokesh_case():
    """Test the specific case: name should be anonymized, aadhaar should be preserved for calculation"""
    
    system = PIIPrivacySystem()
    
    test_text = "i am lokesh sutar i want you to calculate the addition of my aadhaar number aadhaar : 765297568120"
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*50)
    
    result = system.process(test_text, include_llm=False)
    
    print("Anonymized text:")
    print(result.anonymized_text)
    print("\n" + "="*50)
    
    print("Detected entities:")
    for entity in result.entities:
        status = "PRESERVED" if entity.preserve else "ANONYMIZED"
        print(f"- {entity.text} ({entity.label}) -> {status}")
    
    print("\n" + "="*50)
    
    # Check if name was anonymized
    name_anonymized = "lokesh sutar" not in result.anonymized_text.lower()
    
    # Check if aadhaar was preserved
    aadhaar_preserved = "765297568120" in result.anonymized_text
    
    print("Test Results:")
    print(f"Name anonymized: {name_anonymized}")
    print(f"Aadhaar preserved for calculation: {aadhaar_preserved}")
    
    print("\nAnalysis:")
    print(f"- Original: 'lokesh sutar' found in result: {'lokesh sutar' in result.anonymized_text.lower()}")
    print(f"- Original: '765297568120' found in result: {'765297568120' in result.anonymized_text}")
    
    if name_anonymized and aadhaar_preserved:
        print("\nSUCCESS: Mixed context handling works correctly!")
    else:
        print("\nISSUE: Mixed context handling needs adjustment")
        print("Expected: Name should be anonymized, Aadhaar should be preserved for calculation")

if __name__ == "__main__":
    test_lokesh_case()
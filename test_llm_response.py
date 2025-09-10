#!/usr/bin/env python3

from src.core.pii_system import PIIPrivacySystem

def test_llm_response():
    """Test the LLM response for calculation requests"""
    
    system = PIIPrivacySystem()
    
    test_text = "i am lokesh sutar i want you to calculate the addition of my aadhaar number aadhaar : 765297568120"
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*50)
    
    result = system.process(test_text, include_llm=True)
    
    print("Anonymized text:")
    print(result.anonymized_text)
    print("\n" + "="*50)
    
    print("LLM Response:")
    print(result.llm_response)
    print("\n" + "="*50)
    
    print("Reconstructed text:")
    print(result.reconstructed_text)

if __name__ == "__main__":
    test_llm_response()
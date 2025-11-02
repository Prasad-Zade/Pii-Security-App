# -*- coding: utf-8 -*-
"""
Integration test for Faker masking with model wrapper
"""

from model_wrapper import get_model_wrapper


def test_integration():
    """Test Faker masking integration with model wrapper"""
    
    wrapper = get_model_wrapper()
    
    test_cases = [
        "My name is Alice and email is alice@example.com",
        "Call me at 9876543210 for urgent matters",
        "My Aadhaar number is 123456789012",
        "Contact john@test.com or call 5551234567",
    ]
    
    print("=" * 80)
    print("FAKER MASKING INTEGRATION TEST")
    print("=" * 80)
    print(f"Model Status: {wrapper.get_status()}")
    print("=" * 80)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        print(f"Query: {query}")
        
        result = wrapper.process_query(query)
        
        print(f"Masked: {result['masked_query']}")
        print(f"Detected: {', '.join(result['detected_entities'])}")
        print(f"Response: {result['final_response'][:100]}...")
        print(f"Privacy: {'Protected' if result['privacy_preserved'] else 'Not Protected'}")
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    test_integration()

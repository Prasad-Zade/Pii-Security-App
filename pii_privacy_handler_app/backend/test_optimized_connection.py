#!/usr/bin/env python3
"""
Test script to verify optimized backend connection
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    print("✅ Health check passed")

def test_name_introduction():
    """Test name introduction (non-dependent PII)"""
    print("\n" + "="*50)
    print("TEST 2: Name Introduction (Non-dependent PII)")
    print("="*50)
    
    # Create session
    session_response = requests.post(f'{BASE_URL}/sessions', json={'title': 'Test Session'})
    session_id = session_response.json()['id']
    print(f"Session ID: {session_id}")
    
    # Send message
    message = "Hi, my name is Prasad"
    print(f"Input: {message}")
    
    response = requests.post(
        f'{BASE_URL}/sessions/{session_id}/messages',
        json={'text': message}
    )
    
    data = response.json()
    print(f"\nOriginal: {data['user_message']}")
    print(f"Masked: {data['anonymized_text']}")
    print(f"LLM Response: {data['llm_response_reconstructed']}")
    print(f"Entities Detected: {data['detected_entities']}")
    print(f"Entities Masked: {data['entities_masked']}")
    
    assert 'Prasad' not in data['anonymized_text'], "Name should be masked"
    assert len(data['llm_response_reconstructed']) > 0, "Should have LLM response"
    print("✅ Name introduction test passed")

def test_phone_calculation():
    """Test phone calculation (dependent PII)"""
    print("\n" + "="*50)
    print("TEST 3: Phone Calculation (Dependent PII)")
    print("="*50)
    
    # Create session
    session_response = requests.post(f'{BASE_URL}/sessions', json={'title': 'Test Session 2'})
    session_id = session_response.json()['id']
    
    # Send message
    message = "My phone is 9876543210, add all digits"
    print(f"Input: {message}")
    
    response = requests.post(
        f'{BASE_URL}/sessions/{session_id}/messages',
        json={'text': message}
    )
    
    data = response.json()
    print(f"\nOriginal: {data['user_message']}")
    print(f"Masked: {data['anonymized_text']}")
    print(f"LLM Response: {data['llm_response_reconstructed']}")
    print(f"Entities Detected: {data['detected_entities']}")
    print(f"Entities Preserved: {data['entities_preserved']}")
    
    assert '9876543210' in data['anonymized_text'], "Phone should be preserved for calculation"
    assert '45' in data['llm_response_reconstructed'] or 'sum' in data['llm_response_reconstructed'].lower(), "Should calculate digit sum"
    print("✅ Phone calculation test passed")

def test_mixed_pii():
    """Test mixed PII (dependent + non-dependent)"""
    print("\n" + "="*50)
    print("TEST 4: Mixed PII")
    print("="*50)
    
    # Create session
    session_response = requests.post(f'{BASE_URL}/sessions', json={'title': 'Test Session 3'})
    session_id = session_response.json()['id']
    
    # Send message
    message = "I am John, my phone is 1234567890, calculate digit sum"
    print(f"Input: {message}")
    
    response = requests.post(
        f'{BASE_URL}/sessions/{session_id}/messages',
        json={'text': message}
    )
    
    data = response.json()
    print(f"\nOriginal: {data['user_message']}")
    print(f"Masked: {data['anonymized_text']}")
    print(f"LLM Response: {data['llm_response_reconstructed']}")
    print(f"Entities Detected: {data['detected_entities']}")
    print(f"Entities Masked: {data['entities_masked']}")
    print(f"Entities Preserved: {data['entities_preserved']}")
    
    assert 'John' not in data['anonymized_text'], "Name should be masked"
    assert '1234567890' in data['anonymized_text'], "Phone should be preserved"
    print("✅ Mixed PII test passed")

if __name__ == '__main__':
    try:
        print("\n🚀 Starting Optimized Backend Connection Tests")
        print("Make sure backend is running on http://127.0.0.1:5000")
        
        test_health()
        test_name_introduction()
        test_phone_calculation()
        test_mixed_pii()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        print("\nBackend is optimized and working correctly!")
        print("You can now run the Flutter app.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\nMake sure:")
        print("1. Backend is running: python start_with_llm.py")
        print("2. Port 5000 is not blocked")
        print("3. Gemini API key is valid")

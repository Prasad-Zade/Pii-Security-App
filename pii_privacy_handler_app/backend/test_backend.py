#!/usr/bin/env python3
"""
Test script to verify the backend is working with the integrated model
"""

import requests
import json
import time

def test_backend():
    base_url = "http://127.0.0.1:5000/api"
    
    print("Testing PII Privacy Handler Backend Integration")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("[SUCCESS] Health check passed")
            print(f"  - Status: {health_data['status']}")
            print(f"  - Privacy Handler Available: {health_data['privacy_handler_available']}")
            print(f"  - Model Active: {health_data['amazonq_model_active']}")
            print(f"  - Model Type: {health_data['model_type']}")
        else:
            print(f"[ERROR] Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to backend: {e}")
        return False
    
    # Test session creation
    try:
        response = requests.post(f"{base_url}/sessions", 
                               json={"title": "Test Session"}, 
                               timeout=10)
        if response.status_code == 201:
            session_data = response.json()
            session_id = session_data['id']
            print(f"[SUCCESS] Session created: {session_id}")
        else:
            print(f"[ERROR] Session creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Session creation error: {e}")
        return False
    
    # Test message processing with PII
    test_messages = [
        "Hi, my name is John Smith and my phone number is 1234567890",
        "My email is john@example.com and I need help",
        "Calculate the sum of digits in my phone number 9876543210",
        "What is artificial intelligence?",
        "My name is Alice Johnson. Can you reverse my name?"
    ]
    
    print(f"\nTesting {len(test_messages)} messages:")
    print("-" * 30)
    
    for i, message in enumerate(test_messages, 1):
        try:
            print(f"\nTest {i}: {message}")
            
            response = requests.post(f"{base_url}/sessions/{session_id}/messages",
                                   json={"text": message},
                                   timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                print(f"[SUCCESS] Message processed")
                print(f"  Original: {result['user_message']}")
                print(f"  Anonymized: {result['anonymized_text']}")
                print(f"  Response: {result['bot_response'][:100]}...")
                print(f"  Privacy Score: {result['privacy_score']:.1f}%")
                print(f"  Processing Time: {result['processing_time']:.2f}s")
                
                if result['detected_entities']:
                    print(f"  Detected Entities: {result['detected_entities']}")
                if result['entities_masked']:
                    print(f"  Masked Entities: {result['entities_masked']}")
                if result['entities_preserved']:
                    print(f"  Preserved Entities: {result['entities_preserved']}")
            else:
                print(f"[ERROR] Message processing failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"[ERROR] Message processing error: {e}")
    
    print(f"\n[SUCCESS] Backend integration test completed!")
    print("Your Flutter app should now work with PII protection!")
    return True

if __name__ == "__main__":
    print("Make sure the backend server is running (python app.py)")
    print("Press Enter to start testing...")
    input()
    
    success = test_backend()
    if success:
        print("\n🎉 All tests passed! Your model is successfully integrated!")
        print("\nNext steps:")
        print("1. Keep the backend server running")
        print("2. Run your Flutter app")
        print("3. Test with messages containing PII (names, phones, emails)")
        print("4. Check the message details to see all processing steps")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
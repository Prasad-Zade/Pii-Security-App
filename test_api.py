#!/usr/bin/env python3
"""
Test script for PII Privacy Protection API
"""

import requests
import json
import time

# Configuration
BASE_URL = "https://pii-security-app.onrender.com/api"  # Update when deployed
LOCAL_URL = "http://localhost:5000/api"

def test_api(base_url):
    print(f"Testing API at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {e}")
    
    print()
    
    # Test 2: Process Text
    print("2. Testing text processing...")
    test_data = {
        "text": "Customer John Smith, order ID ORD123, count letters in John Smith's name"
    }
    
    try:
        response = requests.post(
            f"{base_url}/process", 
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Text processing successful")
            print(f"  Original: {result['original_text']}")
            print(f"  Masked: {result['masked_text']}")
            print(f"  Privacy Score: {result['privacy_score']}%")
            print(f"  Processing Time: {result['processing_time']}s")
        else:
            print(f"✗ Text processing failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Text processing error: {e}")
    
    print()
    
    # Test 3: Flutter API - Create Session
    print("3. Testing Flutter API - Create Session...")
    try:
        session_data = {"title": "Test Session"}
        response = requests.post(
            f"{base_url}/sessions",
            json=session_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            session_result = response.json()
            print("✓ Session creation successful")
            session_id = session_result['data']['id']
            print(f"  Session ID: {session_id}")
            
            # Test 4: Process in Session
            print("\n4. Testing session processing...")
            process_data = {"text": "User Jane Doe, what's artificial intelligence?"}
            response = requests.post(
                f"{base_url}/sessions/{session_id}/process",
                json=process_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Session processing successful")
                print(f"  Privacy Score: {result['data']['privacy_score']}%")
            else:
                print(f"✗ Session processing failed: {response.status_code}")
        else:
            print(f"✗ Session creation failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Session API error: {e}")
    
    print()

def main():
    print("PII Privacy Protection API Test")
    print("=" * 50)
    
    # Test local first
    print("Testing LOCAL API...")
    test_api(LOCAL_URL)
    
    print("\n" + "=" * 50)
    
    # Test production
    print("Testing PRODUCTION API...")
    test_api(BASE_URL)
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()
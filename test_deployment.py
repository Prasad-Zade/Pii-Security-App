#!/usr/bin/env python3
"""Quick test script for deployment verification"""

import requests
import json

def test_deployment():
    base_url = "https://pii-security-app.onrender.com"
    
    print("🧪 Testing PII Privacy Protection System Deployment")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
    
    # Test 2: Process text
    try:
        test_data = {"text": "Customer John Smith, what is artificial intelligence?"}
        response = requests.post(
            f"{base_url}/api/process",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Text processing: PASSED")
            print(f"   Original: {result['original_text']}")
            print(f"   Masked: {result['masked_text']}")
            print(f"   Privacy Score: {result['privacy_score']}%")
        else:
            print(f"❌ Text processing: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Text processing: ERROR - {e}")
    
    # Test 3: Create session
    try:
        response = requests.post(
            f"{base_url}/api/sessions",
            json={"title": "Test Session"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Session creation: PASSED")
        else:
            print(f"❌ Session creation: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Session creation: ERROR - {e}")
    
    print("\n🎉 Deployment test completed!")
    print("📱 Flutter app can now connect to the API")

if __name__ == "__main__":
    test_deployment()
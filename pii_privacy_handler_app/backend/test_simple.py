#!/usr/bin/env python3
"""Simple test to verify backend is working"""

import requests
import json

def test_connection():
    """Test if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print("\nTo start the backend, run:")
        print("  python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_message():
    """Test sending a message"""
    try:
        # Create session
        session_resp = requests.post(
            "http://127.0.0.1:5000/api/sessions",
            json={"title": "Test"},
            timeout=5
        )
        session_id = session_resp.json()['id']
        print(f"\n✅ Session created: {session_id}")
        
        # Send message
        msg_resp = requests.post(
            f"http://127.0.0.1:5000/api/sessions/{session_id}/messages",
            json={"text": "My name is John and my phone is 1234567890"},
            timeout=10
        )
        
        if msg_resp.status_code == 200:
            result = msg_resp.json()
            print("\n✅ Message processed successfully!")
            print(f"Original: {result['user_message']}")
            print(f"Masked: {result['anonymized_text']}")
            print(f"Response: {result['bot_response'][:100]}...")
            return True
        else:
            print(f"❌ Message failed: {msg_resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Connection Test")
    print("=" * 50)
    
    if test_connection():
        test_message()
    else:
        print("\n⚠️  Start the backend first with: python app.py")

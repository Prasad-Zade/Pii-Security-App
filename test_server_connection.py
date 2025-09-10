#!/usr/bin/env python3
import requests
import json

def test_server_connection():
    """Test connection to the hosted PII server"""
    base_url = "https://pii-security-app.onrender.com"
    
    # Test data
    test_text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    
    try:
        # Test anonymize endpoint
        print("Testing /anonymize endpoint...")
        response = requests.post(
            f"{base_url}/anonymize",
            headers={'Content-Type': 'application/json'},
            json={'text': test_text},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Anonymized text: {data.get('anonymized_text', 'No result')}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_server_connection()
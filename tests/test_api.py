#!/usr/bin/env python3
"""
Test script to validate API server functionality
"""

import requests
import json
import time

def test_api_consistency():
    """Test API endpoint consistency"""
    base_url = "http://localhost:5000"
    
    test_cases = [
        "My name is Alice Johnson and my phone is 555-0123",
        "Contact Dr. Smith at smith@hospital.com for diabetes treatment",
        "SSN: 123-45-6789, Credit Card: 4532-1234-5678-9012"
    ]
    
    print("Testing API Consistency")
    print("=" * 40)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_text}")
        print("-" * 30)
        
        # Test multiple requests
        results = []
        for run in range(3):
            try:
                response = requests.post(
                    f"{base_url}/api/process",
                    json={"text": test_text},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        result_data = data['data']
                        results.append({
                            'anonymized': result_data['anonymized_text'],
                            'privacy_score': result_data['privacy_score']
                        })
                        print(f"Run {run + 1}: Score {result_data['privacy_score']}")
                    else:
                        print(f"Run {run + 1}: API Error - {data.get('error', 'Unknown')}")
                else:
                    print(f"Run {run + 1}: HTTP {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Run {run + 1}: Connection Error - {e}")
            
            time.sleep(0.1)  # Small delay between requests
        
        # Check consistency
        if len(results) == 3:
            anonymized_texts = [r['anonymized'] for r in results]
            scores = [r['privacy_score'] for r in results]
            
            if len(set(anonymized_texts)) == 1 and len(set(scores)) == 1:
                print("[PASS] API responses are consistent")
            else:
                print("[FAIL] API responses are inconsistent")
        else:
            print(f"[WARN] Only {len(results)}/3 requests succeeded")

if __name__ == "__main__":
    print("Make sure the API server is running on localhost:5000")
    print("Start it with: python api_server.py")
    print()
    
    try:
        # Quick health check
        response = requests.get("http://localhost:5000/api/sessions", timeout=5)
        if response.status_code == 200:
            test_api_consistency()
        else:
            print("API server not responding correctly")
    except requests.exceptions.RequestException:
        print("Cannot connect to API server. Make sure it's running on localhost:5000")
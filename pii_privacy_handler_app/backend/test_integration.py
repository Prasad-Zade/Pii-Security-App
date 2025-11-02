#!/usr/bin/env python3
"""
Test script to verify the integration between Flutter app and AmazonQ Model V1
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_backend_health():
    """Test if backend is running and healthy"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy")
            print(f"   Privacy Handler Available: {data.get('privacy_handler_available', False)}")
            print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_session_creation():
    """Test session creation"""
    print("\n🔍 Testing session creation...")
    try:
        payload = {"title": "Test Session"}
        response = requests.post(f"{BASE_URL}/sessions", 
                               json=payload, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code == 201:
            session = response.json()
            print(f"✅ Session created successfully")
            print(f"   Session ID: {session.get('id', 'N/A')}")
            print(f"   Title: {session.get('title', 'N/A')}")
            return session.get('id')
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return None

def test_pii_processing(session_id):
    """Test PII processing with various inputs"""
    print(f"\n🔍 Testing PII processing in session {session_id}...")
    
    test_cases = [
        {
            "name": "Basic Name and Email",
            "text": "Hi, my name is John Smith and my email is john.smith@company.com"
        },
        {
            "name": "Phone Number with Math",
            "text": "My phone number is 1234567890. Can you add all the digits in my phone number?"
        },
        {
            "name": "Aadhaar Number",
            "text": "My Aadhaar number is 123456789012. Please verify it."
        },
        {
            "name": "Multiple PII Types",
            "text": "I am Dr. Sarah Johnson, my email is sarah@hospital.com and my phone is 555-123-4567"
        },
        {
            "name": "Simple Greeting",
            "text": "Hello! How are you today?"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        print(f"   Input: {test_case['text']}")
        
        try:
            payload = {"text": test_case['text']}
            response = requests.post(f"{BASE_URL}/sessions/{session_id}/messages",
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Processed successfully")
                print(f"   Anonymized: {result.get('anonymized_text', 'N/A')}")
                print(f"   Privacy Score: {result.get('privacy_score', 'N/A')}%")
                print(f"   Detected Entities: {result.get('detected_entities', [])}")
                print(f"   Context: {result.get('context', 'N/A')}")
                print(f"   Processing Time: {result.get('processing_time', 'N/A')}s")
                
                # Show bot response (truncated)
                bot_response = result.get('bot_response', 'No response')
                if len(bot_response) > 100:
                    bot_response = bot_response[:100] + "..."
                print(f"   Bot Response: {bot_response}")
                
                results.append({
                    "test_case": test_case['name'],
                    "success": True,
                    "privacy_score": result.get('privacy_score', 0),
                    "detected_entities": result.get('detected_entities', []),
                    "processing_time": result.get('processing_time', 0)
                })
            else:
                print(f"   ❌ Processing failed: {response.status_code}")
                print(f"   Response: {response.text}")
                results.append({
                    "test_case": test_case['name'],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"   ❌ Processing error: {e}")
            results.append({
                "test_case": test_case['name'],
                "success": False,
                "error": str(e)
            })
    
    return results

def test_session_management(session_id):
    """Test session management operations"""
    print(f"\n🔍 Testing session management...")
    
    # Test getting sessions
    try:
        response = requests.get(f"{BASE_URL}/sessions", timeout=10)
        if response.status_code == 200:
            sessions = response.json()
            print(f"✅ Retrieved {len(sessions)} sessions")
        else:
            print(f"❌ Failed to get sessions: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting sessions: {e}")
    
    # Test getting messages
    try:
        response = requests.get(f"{BASE_URL}/sessions/{session_id}/messages", timeout=10)
        if response.status_code == 200:
            messages = response.json()
            print(f"✅ Retrieved {len(messages)} messages from session")
        else:
            print(f"❌ Failed to get messages: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting messages: {e}")

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    successful_tests = [r for r in results if r.get('success', False)]
    failed_tests = [r for r in results if not r.get('success', False)]
    
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if successful_tests:
        avg_privacy_score = sum(r.get('privacy_score', 0) for r in successful_tests) / len(successful_tests)
        avg_processing_time = sum(r.get('processing_time', 0) for r in successful_tests) / len(successful_tests)
        
        print(f"\nPerformance Metrics:")
        print(f"Average Privacy Score: {avg_privacy_score:.1f}%")
        print(f"Average Processing Time: {avg_processing_time:.2f}s")
        
        # Count detected entity types
        all_entities = []
        for r in successful_tests:
            all_entities.extend(r.get('detected_entities', []))
        
        if all_entities:
            entity_counts = {}
            for entity in all_entities:
                entity_counts[entity] = entity_counts.get(entity, 0) + 1
            
            print(f"\nDetected Entity Types:")
            for entity_type, count in sorted(entity_counts.items()):
                print(f"  {entity_type}: {count}")
    
    if failed_tests:
        print(f"\nFailed Tests:")
        for test in failed_tests:
            print(f"  ❌ {test['test_case']}: {test.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)

def main():
    """Main test function"""
    print("🚀 Starting Integration Test")
    print("="*60)
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not available. Please start the backend first.")
        print("   Run: cd backend && python app.py")
        return
    
    # Create test session
    session_id = test_session_creation()
    if not session_id:
        print("\n❌ Cannot proceed without a valid session")
        return
    
    # Test PII processing
    results = test_pii_processing(session_id)
    
    # Test session management
    test_session_management(session_id)
    
    # Print summary
    print_summary(results)
    
    # Cleanup (optional)
    print(f"\n🧹 Cleaning up test session {session_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/sessions/{session_id}", timeout=10)
        if response.status_code == 200:
            print("✅ Test session cleaned up successfully")
        else:
            print(f"⚠️ Failed to cleanup session: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")
    
    print("\n✅ Integration test completed!")

if __name__ == "__main__":
    main()
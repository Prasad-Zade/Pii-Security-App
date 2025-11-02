#!/usr/bin/env python3
"""
Test script to verify model integration
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_model_integration():
    """Test the model wrapper integration"""
    print("🧪 Testing PII Model Integration")
    print("=" * 50)
    
    try:
        from model_wrapper import get_model_wrapper
        
        # Get model wrapper instance
        wrapper = get_model_wrapper()
        
        # Check status
        status = wrapper.get_status()
        print(f"📊 Model Status:")
        print(f"   Model Loaded: {status['model_loaded']}")
        print(f"   Handler Available: {status['handler_available']}")
        print(f"   Model Type: {status['model_type']}")
        print(f"   Model Ready: {status.get('model_ready', 'Unknown')}")
        
        # Test cases
        test_cases = [
            "My name is Prasad Zade and my phone number is 7418529635. Tell me the addition of it.",
            "Hello, I am John Smith from Mumbai",
            "Count letters in name Alice",
            "What is the weather today?"
        ]
        
        print(f"\n🧪 Running Test Cases:")
        print("-" * 50)
        
        for i, query in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {query}")
            
            try:
                result = wrapper.process_query(query)
                
                print(f"   🎭 Masked: {result['masked_query']}")
                print(f"   🔍 Detected: {result['detected_entities']}")
                print(f"   🔒 Masked Entities: {result['entities_masked']}")
                print(f"   🔓 Preserved: {result['entities_preserved']}")
                print(f"   🏷️ Context: {result['context']}")
                print(f"   🛡️ Privacy Preserved: {result['privacy_preserved']}")
                print(f"   🤖 Response: {result['final_response'][:100]}...")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n✅ Integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    test_model_integration()
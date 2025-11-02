#!/usr/bin/env python3
"""
Startup script for the PII Privacy Handler Backend
"""

import os
import sys
from app import app, model_wrapper

def main():
    print("🚀 Starting PII Privacy Handler Backend")
    print("=" * 50)
    
    # Check model status
    model_status = model_wrapper.get_status()
    print(f"📊 Model Status:")
    print(f"   - Model Loaded: {model_status['model_loaded']}")
    print(f"   - Handler Available: {model_status['handler_available']}")
    print(f"   - Model Type: {model_status['model_type']}")
    
    # Test model with a sample query
    print(f"\n🧪 Testing model with sample query...")
    try:
        test_result = model_wrapper.process_query("Hi, my name is John and my phone is 1234567890")
        print(f"   - Original: {test_result['original_query']}")
        print(f"   - Masked: {test_result['masked_query']}")
        print(f"   - Entities: {test_result['detected_entities']}")
        print(f"   - Response: {test_result['final_response'][:50]}...")
        print(f"✅ Model test successful!")
    except Exception as e:
        print(f"❌ Model test failed: {e}")
    
    # Start server
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🌐 Starting server on port {port}")
    print(f"📱 Flutter app can connect to: http://127.0.0.1:{port}/api")
    print(f"🔗 Health check: http://127.0.0.1:{port}/api/health")
    print(f"\n💡 Keep this terminal open while using the Flutter app")
    print("=" * 50)
    
    try:
        app.run(debug=False, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print(f"\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main()
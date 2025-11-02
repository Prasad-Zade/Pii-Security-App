#!/usr/bin/env python3
"""
Startup script for PII Privacy Handler with trained model
"""

import os
import sys
import subprocess

def check_model_files():
    """Check if trained model files exist"""
    print("🔍 Checking for trained model files...")
    
    # Get paths
    backend_dir = os.path.dirname(__file__)
    app_dir = os.path.dirname(backend_dir)
    security_app_dir = os.path.dirname(app_dir)
    amazonq_root = os.path.dirname(security_app_dir)
    model_dir = os.path.join(amazonq_root, 'AmazonQ_modelv1', 'AmazonQ_model')
    
    # Check key files
    key_files = [
        os.path.join(model_dir, 'final_project_model.py'),
        os.path.join(model_dir, 'src', 'privacy_handler.py'),
        os.path.join(model_dir, 'src', 'pii_detector.py'),
        os.path.join(model_dir, 'models', 'final_pii_model.pkl')
    ]
    
    missing_files = []
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"   ✅ {os.path.basename(file_path)}")
        else:
            print(f"   ❌ {os.path.basename(file_path)} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Some model files are missing. The system will use fallback handlers.")
        return False
    
    print("✅ All model files found!")
    return True

def test_model_loading():
    """Test if the model can be loaded"""
    print("\n🧪 Testing model loading...")
    
    try:
        # Test the integration
        result = subprocess.run([
            sys.executable, 'test_model_integration.py'
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Model integration test passed!")
            print(result.stdout)
            return True
        else:
            print("❌ Model integration test failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting PII Privacy Handler Server...")
    print("=" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'], cwd=os.path.dirname(__file__))
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🔒 PII Privacy Handler - Startup with Trained Model")
    print("=" * 60)
    
    # Check model files
    model_files_ok = check_model_files()
    
    # Test model loading
    if model_files_ok:
        model_loading_ok = test_model_loading()
        if not model_loading_ok:
            print("⚠️  Model loading failed, but server will start with fallback handlers")
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
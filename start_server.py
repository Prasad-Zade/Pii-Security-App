#!/usr/bin/env python3
"""
Simple script to start the PII Privacy Server
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    return True

def start_server():
    """Start the Flask server"""
    print("\n" + "="*50)
    print("🚀 Starting PII Privacy Server")
    print("="*50)
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    try:
        # Change to the directory containing the script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Start the server
        subprocess.run([sys.executable, "api_server.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")

if __name__ == "__main__":
    if install_requirements():
        start_server()
    else:
        print("Failed to start server due to dependency issues")
        input("Press Enter to exit...")
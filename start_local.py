#!/usr/bin/env python3
"""
Local development startup script
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'transformers', 'torch', 
        'scikit-learn', 'numpy', 'spacy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    return True

def download_spacy_model():
    """Download spaCy model if not present"""
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("✓ spaCy model already available")
    except OSError:
        print("Downloading spaCy model...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

def main():
    print("PII Privacy Protection System - Local Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Download spaCy model
    download_spacy_model()
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("\nStarting local development server...")
    print("Web Interface: http://localhost:5000")
    print("API Base URL: http://localhost:5000/api")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
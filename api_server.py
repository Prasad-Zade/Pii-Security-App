#!/usr/bin/env python3
"""Redirect to main app.py for Render compatibility"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting PII Privacy Protection System on port {port}")
    print("📊 Functional model integration active")
    app.run(host='0.0.0.0', port=port, debug=False)
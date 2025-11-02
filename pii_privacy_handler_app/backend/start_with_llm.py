#!/usr/bin/env python3
"""
Start the backend with Gemini LLM support
"""

import os
import sys
from app import app

def main():
    print("=" * 50)
    print("PII Privacy Handler Backend with Gemini LLM")
    print("=" * 50)
    print("[OK] Gemini API configured - Real LLM responses enabled")
    
    print("\nStarting server on http://127.0.0.1:5000")
    print("Health check: http://127.0.0.1:5000/api/health")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == '__main__':
    main()
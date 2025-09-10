#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_math_patterns():
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    
    mathematical_patterns = [
        r'sum of ([\d\s-]+)',
        r'add ([\d\s-]+)',
        r'total of ([\d\s-]+)',
        r'addition of ([\d\s-]+)',
        r'([\d\s-]+) \+ ([\d\s-]+)',
        r'([\d\s-]+) - ([\d\s-]+)',
        r'([\d\s-]+) \* ([\d\s-]+)',
        r'([\d\s-]+) / ([\d\s-]+)',
        r'what is.*(?:sum|add|total|addition).*([\d\s-]+)',
        r'tell me.*(?:sum|add|total|addition).*([\d\s-]+)',
        r'calculate.*([\d\s-]+)',
        r'compute.*([\d\s-]+)',
    ]
    
    print(f"Text: {text}")
    
    for i, pattern in enumerate(mathematical_patterns):
        matches = re.findall(pattern, text)
        if matches:
            print(f"\nMATCH - Pattern {i}: {pattern}")
            print(f"Matches: {matches}")

if __name__ == "__main__":
    test_math_patterns()
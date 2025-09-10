#!/usr/bin/env python3
import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.dependency_analyzer import DependencyAnalyzer

def test_direct_reference():
    analyzer = DependencyAnalyzer()
    text = "my name is prasad and my phone number is 1111111111"
    
    # Mock entity
    class MockEntity:
        def __init__(self, text, label):
            self.text = text
            self.label = label
    
    entities = [MockEntity("1111111111", "PHONE")]
    
    dependencies = analyzer.analyze_dependencies(text, entities)
    print(f"Dependencies: {dependencies}")
    
    # Check direct references
    direct_refs = analyzer._find_direct_references(text.lower())
    print(f"Direct references: {direct_refs}")
    
    # Check if phone is directly referenced
    phone_referenced = analyzer._is_directly_referenced("1111111111", direct_refs)
    print(f"Phone directly referenced: {phone_referenced}")

if __name__ == "__main__":
    test_direct_reference()
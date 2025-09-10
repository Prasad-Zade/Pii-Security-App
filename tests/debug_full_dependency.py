#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.dependency_analyzer import DependencyAnalyzer

def test_full_dependency():
    analyzer = DependencyAnalyzer()
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    
    # Mock entities
    class MockEntity:
        def __init__(self, text, label):
            self.text = text
            self.label = label
    
    name_entity = MockEntity("prasad", "PERSON")
    phone_entity = MockEntity("1111111111", "PHONE")
    
    # Test each entity individually
    print("=== NAME ENTITY ===")
    print(f"Text: {text}")
    print(f"Entity: {name_entity.text} ({name_entity.label})")
    
    # Test calculation context
    name_calc_context = analyzer._is_in_calculation_context(name_entity.text, text)
    print(f"In calculation context: {name_calc_context}")
    
    print("\n=== PHONE ENTITY ===")
    print(f"Entity: {phone_entity.text} ({phone_entity.label})")
    
    # Test calculation context
    phone_calc_context = analyzer._is_in_calculation_context(phone_entity.text, text)
    print(f"In calculation context: {phone_calc_context}")

if __name__ == "__main__":
    test_full_dependency()
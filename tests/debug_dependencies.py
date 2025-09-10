#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.dependency_analyzer import DependencyAnalyzer

def test_dependencies():
    analyzer = DependencyAnalyzer()
    text = "my name is prasad and my phone number is 1111111111 tell me addition of it"
    
    # Mock entities
    class MockEntity:
        def __init__(self, text, label):
            self.text = text
            self.label = label
    
    entities = [
        MockEntity("prasad", "PERSON"),
        MockEntity("1111111111", "PHONE")
    ]
    
    dependencies = analyzer.analyze_dependencies(text, entities)
    print(f"Dependencies found: {dependencies}")
    
    # Test each entity preservation
    for entity in entities:
        entity_key = f"{entity.label}:{entity.text}"
        should_preserve = analyzer.should_preserve_entity(entity, text, dependencies)
        print(f"\nEntity: {entity.text} ({entity.label})")
        print(f"Key: {entity_key}")
        print(f"Dependencies: {dependencies.get(entity_key, 'None')}")
        print(f"Should preserve: {should_preserve}")

if __name__ == "__main__":
    test_dependencies()
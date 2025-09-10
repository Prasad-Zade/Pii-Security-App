#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_comprehensive_names():
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        # Basic patterns
        "my name is prasad zade",
        "I am John Smith", 
        "I'm Sarah Johnson",
        "call me Mike Davis",
        "this is Raj Patel",
        "here is Priya Sharma",
        
        # Formal introductions
        "name: David Wilson",
        "full name is Maria Garcia",
        "first name is Alex",
        "last name is Thompson", 
        "surname is Anderson",
        "I'm called Robert Brown",
        "they call me Lisa White",
        "known as Jennifer Taylor",
        "goes by Michael Jackson",
        "named after Elizabeth Moore",
        
        # Standalone names
        "Hello, I'm Amit Kumar and I work here",
        "Please contact Sneha Reddy for details",
        "The manager is Vikram Singh",
        "Dr. Rajesh Gupta will see you",
        
        # Names with special characters
        "my name is Mary-Jane Watson",
        "I am O'Connor Patrick",
        "call me Jean-Luc Picard",
        
        # Multiple names in text
        "I am John Doe and my colleague is Jane Smith",
        "Contact either Rahul Sharma or Neha Patel",
        
        # Edge cases that should NOT be detected as names
        "I live in New York",
        "Visit Los Angeles soon",
        "The United States is large",
        "Go to Main Street",
        
        # Non-English names
        "my name is Zhang Wei",
        "I am Hiroshi Tanaka", 
        "call me Abdul Rahman",
        "this is Olumide Adebayo"
    ]
    
    print("Comprehensive Name Detection Test")
    print("=" * 60)
    
    for i, test_text in enumerate(test_cases, 1):
        result = pii_system.process(test_text, include_llm=False)
        person_entities = [e for e in result.entities if e.label == 'PERSON']
        
        print(f"\n{i:2d}. {test_text}")
        if person_entities:
            for entity in person_entities:
                print(f"    -> Detected: '{entity.text}' (confidence: {entity.confidence})")
            print(f"    -> Result: {result.anonymized_text}")
        else:
            print("    -> No names detected")

if __name__ == "__main__":
    test_comprehensive_names()
#!/usr/bin/env python3
"""
Test script for PII Dependency Handler
Demonstrates dependent vs non-dependent PII handling
"""

from pii_dependency_handler import PIIDependencyHandler

def test_pii_dependency():
    handler = PIIDependencyHandler()
    
    print("=" * 60)
    print("PII DEPENDENCY HANDLER TEST")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Dependent Test Case",
            "query": "My name is Prasad and my phone number is 7418529635. Tell me the addition of it.",
            "description": "Phone number is needed for computation, name is not"
        },
        {
            "name": "Non-Dependent Test Case", 
            "query": "My name is Prasad and my phone number is 7418529635.",
            "description": "Both name and phone are just for identification"
        },
        {
            "name": "Mixed Dependency Case",
            "query": "Hi, I'm John with phone 9876543210 and email john@test.com. Calculate the sum of my phone digits.",
            "description": "Phone needed for calculation, name and email are not"
        },
        {
            "name": "No PII Case",
            "query": "What is the weather like today?",
            "description": "No personal information present"
        },
        {
            "name": "Phone Calculation Only",
            "query": "Calculate the sum of digits in 5551234567.",
            "description": "Phone number used directly in calculation"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   Query: \"{test_case['query']}\"")
        print("-" * 50)
        
        result = handler.process_query(test_case['query'])
        
        print(f"   Original:     {result['original_query']}")
        print(f"   Masked:       {result['masked_query']}")
        print(f"   Context:      {result['context']}")
        print(f"   Privacy Score: {result['privacy_score']:.1f}%")
        
        if result['dependent_entities']:
            print(f"   Dependent PII (kept):     {[e['type'] + ':' + e['value'] for e in result['dependent_entities']]}")
        
        if result['non_dependent_entities']:
            print(f"   Non-Dependent PII (masked): {[e['type'] + ':' + e['value'] for e in result['non_dependent_entities']]}")
        
        print(f"   Response:     {result['final_response']}")
        print()

if __name__ == "__main__":
    test_pii_dependency()
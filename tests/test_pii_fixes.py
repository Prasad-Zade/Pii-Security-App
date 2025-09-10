#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify PII detection and anonymization consistency
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.pii_system import PIIPrivacySystem

def test_consistency():
    """Test that the same input produces consistent results"""
    pii_system = PIIPrivacySystem()
    
    test_cases = [
        "My name is John Doe and my email is john.doe@gmail.com",
        "Call me at 555-123-4567 or email sarah.smith@company.com",
        "Dr. Michael Johnson works at Microsoft in Seattle",
        "Patient has diabetes and hypertension, contact at 123-45-6789",
        "IP address 192.168.1.1 accessed by user@domain.org"
    ]
    
    print("Testing PII Detection and Anonymization Consistency")
    print("=" * 60)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_text}")
        print("-" * 40)
        
        # Run the same text multiple times to check consistency
        results = []
        for run in range(3):
            result = pii_system.process(test_text, include_llm=False)
            results.append(result)
            print(f"Run {run + 1}:")
            print(f"  Entities: {len(result.entities)}")
            print(f"  Anonymized: {result.anonymized_text}")
            print(f"  Privacy Score: {result.privacy_score}")
        
        # Check consistency
        anonymized_texts = [r.anonymized_text for r in results]
        entity_counts = [len(r.entities) for r in results]
        
        if len(set(anonymized_texts)) == 1 and len(set(entity_counts)) == 1:
            print("[PASS] CONSISTENT - All runs produced identical results")
        else:
            print("[FAIL] INCONSISTENT - Results varied between runs")
            print(f"   Anonymized texts: {set(anonymized_texts)}")
            print(f"   Entity counts: {set(entity_counts)}")

if __name__ == "__main__":
    test_consistency()
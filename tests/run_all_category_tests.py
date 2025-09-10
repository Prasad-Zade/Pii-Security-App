#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test_medical_scenarios import test_medical_scenarios
from test_financial_scenarios import test_financial_scenarios
from test_computational_scenarios import test_computational_scenarios
from test_contact_scenarios import test_contact_scenarios
from test_government_id_scenarios import test_government_id_scenarios

def run_all_category_tests():
    """Run all categorized test scenarios"""
    print("PII PRIVACY PROTECTION SYSTEM - COMPREHENSIVE CATEGORY TESTS")
    print("=" * 70)
    
    total_correct = 0
    total_tests = 0
    
    # Medical scenarios
    print("\n1. MEDICAL SCENARIOS")
    print("-" * 30)
    correct, tests = test_medical_scenarios()
    total_correct += correct
    total_tests += tests
    
    # Financial scenarios
    print("\n2. FINANCIAL SCENARIOS")
    print("-" * 30)
    correct, tests = test_financial_scenarios()
    total_correct += correct
    total_tests += tests
    
    # Computational scenarios
    print("\n3. COMPUTATIONAL SCENARIOS")
    print("-" * 30)
    correct, tests = test_computational_scenarios()
    total_correct += correct
    total_tests += tests
    
    # Contact scenarios
    print("\n4. CONTACT SCENARIOS")
    print("-" * 30)
    correct, tests = test_contact_scenarios()
    total_correct += correct
    total_tests += tests
    
    # Government ID scenarios
    print("\n5. GOVERNMENT ID SCENARIOS")
    print("-" * 30)
    correct, tests = test_government_id_scenarios()
    total_correct += correct
    total_tests += tests
    
    # Overall results
    print("\n" + "=" * 70)
    print(f"OVERALL ACCURACY: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    print("=" * 70)
    
    return total_correct/total_tests*100

if __name__ == "__main__":
    run_all_category_tests()
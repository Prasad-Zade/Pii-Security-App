import 'lib/services/pii_dependency_analyzer.dart';

void main() {
  print("=" * 80);
  print("COMPREHENSIVE PII DEPENDENCY TEST SUITE");
  print("=" * 80);
  
  final testCases = [
    // DEPENDENT TEST CASES (PII needed for computation)
    {
      "category": "DEPENDENT",
      "name": "Phone Addition",
      "input": "My name is John Smith and my phone number is 7418529635. Tell me the addition of it.",
      "expected": "Name masked, phone kept for calculation"
    },
    {
      "category": "DEPENDENT", 
      "name": "Phone Sum",
      "input": "I'm Sarah Johnson, phone 9876543210. Calculate the sum of digits.",
      "expected": "Name masked, phone kept for calculation"
    },
    {
      "category": "DEPENDENT",
      "name": "Multiple Numbers Calculation", 
      "input": "My name is Alex Brown, numbers are 1234567890 and 9876543210. Add them.",
      "expected": "Name masked, phones kept for calculation"
    },
    
    // NON-DEPENDENT TEST CASES (PII only for identification)
    {
      "category": "NON-DEPENDENT",
      "name": "Simple Introduction",
      "input": "My name is David Wilson and my phone number is 5551234567.",
      "expected": "Both name and phone masked"
    },
    {
      "category": "NON-DEPENDENT",
      "name": "Travel Query",
      "input": "My name is Lisa Davis I want to visit Paris tell me where to visit",
      "expected": "Name masked, Paris preserved"
    },
    {
      "category": "NON-DEPENDENT",
      "name": "Email Introduction",
      "input": "I'm Michael Chen, my email is mike@gmail.com and I need help",
      "expected": "Name and email masked"
    },
    
    // MIXED DEPENDENCY TEST CASES
    {
      "category": "MIXED",
      "name": "Address with Calculation",
      "input": "My name is Emma Taylor, I live at 123 Oak Street, phone 7418529635. Calculate phone digits.",
      "expected": "Name and address masked, phone kept"
    },
    {
      "category": "MIXED",
      "name": "Multiple PII Types",
      "input": "Hi, I'm Robert Johnson, phone 5551234567, email rob@yahoo.com, visiting Tokyo",
      "expected": "Name and email masked, phone masked (no calculation)"
    },
    
    // EDGE CASES
    {
      "category": "EDGE",
      "name": "No PII",
      "input": "What is the weather like in London today?",
      "expected": "No masking needed"
    },
    {
      "category": "EDGE",
      "name": "Detailed Address",
      "input": "My name is Jennifer Smith I live at 456 Elm Avenue New York",
      "expected": "Name and detailed address masked, city preserved"
    }
  ];
  
  int testNumber = 1;
  int passedTests = 0;
  int failedTests = 0;
  
  for (var testCase in testCases) {
    print("\n${testNumber}. [${testCase['category']}] ${testCase['name']}");
    print("Input: \"${testCase['input']}\"");
    print("Expected: ${testCase['expected']}");
    print("-" * 60);
    
    try {
      final result = PIIDependencyAnalyzer.analyzeQuery(testCase['input'] as String);
      
      print("Original:  ${result['originalQuery']}");
      print("Masked:    ${result['maskedQuery']}");
      print("Privacy Score: ${(result['privacyScore'] * 100).toStringAsFixed(1)}%");
      
      final dependentEntities = result['dependentEntities'] as List;
      final nonDependentEntities = result['nonDependentEntities'] as List;
      
      if (dependentEntities.isNotEmpty) {
        print("Dependent PII (kept):     ${dependentEntities.map((e) => '${e['type']}:${e['value']}').join(', ')}");
      }
      
      if (nonDependentEntities.isNotEmpty) {
        print("Non-Dependent PII (masked): ${nonDependentEntities.map((e) => '${e['type']}:${e['value']}').join(', ')}");
      }
      
      if (dependentEntities.isEmpty && nonDependentEntities.isEmpty) {
        print("No PII detected");
      }
      
      // Validate test results
      bool testPassed = _validateTest(testCase, result);
      
      if (testPassed) {
        print("✅ TEST PASSED");
        passedTests++;
      } else {
        print("❌ TEST FAILED");
        failedTests++;
      }
      
    } catch (e) {
      print("❌ TEST ERROR: $e");
      failedTests++;
    }
    
    testNumber++;
  }
  
  print("\n" + "=" * 80);
  print("TEST SUMMARY");
  print("=" * 80);
  print("Total Tests: ${testCases.length}");
  print("Passed: $passedTests");
  print("Failed: $failedTests");
  print("Success Rate: ${(passedTests / testCases.length * 100).toStringAsFixed(1)}%");
  print("=" * 80);
}

bool _validateTest(Map<String, dynamic> testCase, Map<String, dynamic> result) {
  final category = testCase['category'] as String;
  final dependentEntities = result['dependentEntities'] as List;
  final nonDependentEntities = result['nonDependentEntities'] as List;
  final maskedQuery = result['maskedQuery'] as String;
  final originalQuery = result['originalQuery'] as String;
  
  switch (category) {
    case 'DEPENDENT':
      // Should have dependent PII (phone numbers for calculation)
      return dependentEntities.isNotEmpty && 
             dependentEntities.any((e) => e['type'] == 'phone');
             
    case 'NON-DEPENDENT':
      // Should have only non-dependent PII (all masked)
      return dependentEntities.isEmpty && nonDependentEntities.isNotEmpty;
      
    case 'MIXED':
      // Should have both dependent and non-dependent PII
      return dependentEntities.isNotEmpty && nonDependentEntities.isNotEmpty;
      
    case 'EDGE':
      // Special validation for edge cases
      if (testCase['name'] == 'No PII') {
        return dependentEntities.isEmpty && nonDependentEntities.isEmpty;
      }
      return nonDependentEntities.isNotEmpty;
      
    default:
      return false;
  }
}
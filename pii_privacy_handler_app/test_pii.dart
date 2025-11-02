import 'lib/services/pii_dependency_analyzer.dart';

void main() {
  // Test case 1: Non-dependent case
  String test1 = "My name is Prasad and my phone number is 7418529635.";
  var result1 = PIIDependencyAnalyzer.analyzeQuery(test1);
  print("Test 1:");
  print("Input: $test1");
  print("Output: ${result1['maskedQuery']}");
  print("Dependent entities: ${result1['dependentEntities']}");
  print("Non-dependent entities: ${result1['nonDependentEntities']}");
  print("");
  
  // Test case 2: Dependent case
  String test2 = "My name is Prasad and my phone number is 7418529635. Tell me the addition of it.";
  var result2 = PIIDependencyAnalyzer.analyzeQuery(test2);
  print("Test 2:");
  print("Input: $test2");
  print("Output: ${result2['maskedQuery']}");
  print("Dependent entities: ${result2['dependentEntities']}");
  print("Non-dependent entities: ${result2['nonDependentEntities']}");
  print("");
  
  // Test case 3: Place name (should not be masked)
  String test3 = "my name is Piyush Nile I want to visit mumbai tell me where to visit";
  var result3 = PIIDependencyAnalyzer.analyzeQuery(test3);
  print("Test 3 - Place name:");
  print("Input: $test3");
  print("Output: ${result3['maskedQuery']}");
  print("Non-dependent entities: ${result3['nonDependentEntities']}");
  print("");
  
  // Test case 4: Detailed address (should be masked)
  String test4 = "my name is John Smith I live at 123 Main Street New York";
  var result4 = PIIDependencyAnalyzer.analyzeQuery(test4);
  print("Test 4 - Detailed address:");
  print("Input: $test4");
  print("Output: ${result4['maskedQuery']}");
  print("Non-dependent entities: ${result4['nonDependentEntities']}");
}
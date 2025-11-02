# PII Privacy Handler - Dependent vs Non-Dependent Test Cases

## Overview

This PII Privacy Handler implements intelligent privacy protection by distinguishing between **dependent** and **non-dependent** PII entities based on their role in the user's query.

## Key Concepts

### Dependent PII
- **Definition**: PII data that participates in computation, logic, or is essential for providing the requested output
- **Handling**: Preserved in the query to maintain functionality
- **Examples**: Phone numbers used in mathematical calculations, addresses needed for location-based services

### Non-Dependent PII  
- **Definition**: PII data that only appears for identification or context but doesn't affect the core processing
- **Handling**: Masked with generic placeholders to protect privacy
- **Examples**: Names used for greeting, email addresses mentioned in passing

## Test Cases

### 1. Dependent Test Case
```
Input: "My name is Prasad and my phone number is 7418529635. Tell me the addition of it."

Analysis:
- Name "Prasad" → Non-dependent (masked as [NAME])
- Phone "7418529635" → Dependent (kept for calculation)

Output: "My name is [NAME] and my phone number is 7418529635. Tell me the addition of it."
Response: Calculates sum of phone digits while protecting the name
```

### 2. Non-Dependent Test Case
```
Input: "My name is Prasad and my phone number is 7418529635."

Analysis:
- Name "Prasad" → Non-dependent (masked as [NAME])
- Phone "7418529635" → Non-dependent (masked as [PHONE])

Output: "My name is [NAME] and my phone number is [PHONE]."
Response: Both PII entities are masked for privacy protection
```

### 3. Mixed Dependency Case
```
Input: "Hi, I'm John with phone 9876543210 and email john@test.com. Calculate the sum of my phone digits."

Analysis:
- Name "John" → Non-dependent (masked as [NAME])
- Phone "9876543210" → Dependent (kept for calculation)
- Email "john@test.com" → Non-dependent (masked as [EMAIL])

Output: "Hi, I'm [NAME] with phone 9876543210 and email [EMAIL]. Calculate the sum of my phone digits."
Response: Only phone number is preserved for the calculation
```

## Implementation Features

### Frontend (Flutter/Dart)
- **PIIDependencyAnalyzer**: Analyzes queries to detect PII and determine dependencies
- **PIITestScreen**: Interactive test interface to demonstrate functionality
- **Real-time Analysis**: Shows which PII entities are dependent vs non-dependent

### Backend (Python/Flask)
- **PIIDependencyHandler**: Server-side processing with advanced dependency detection
- **Context-Aware Processing**: Understands computational vs informational contexts
- **Intelligent Response Generation**: Provides appropriate responses based on PII handling

## Privacy Score Calculation

The system calculates a privacy score based on:
- Total PII entities detected
- Percentage of entities successfully masked
- Context sensitivity of the processing

```
Privacy Score = (Masked Entities / Total Entities) × 100%
```

## Usage

### Running the Test Interface
1. Start the Flutter app
2. Navigate to the PII Test Screen (science icon)
3. Try the provided test cases or enter custom queries
4. Observe the analysis results showing dependent vs non-dependent classification

### Backend Testing
```bash
cd backend
python test_pii_dependency.py
```

## Security Benefits

1. **Selective Privacy Protection**: Only masks PII that doesn't affect functionality
2. **Maintained Functionality**: Preserves essential data for computations
3. **Context Awareness**: Understands when PII is truly needed vs just mentioned
4. **Transparent Processing**: Shows users exactly what was masked and why

## Supported PII Types

- **Names**: Personal names and identifiers
- **Phone Numbers**: Mobile and landline numbers
- **Email Addresses**: Personal and business emails
- **SSN**: Social Security Numbers
- **Credit Cards**: Payment card numbers

## Future Enhancements

- Machine learning-based dependency detection
- Custom PII type definitions
- User-configurable privacy levels
- Advanced context understanding with NLP models
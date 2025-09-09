# Dependency Preservation System

## Overview
The system now intelligently preserves PII data when it's referenced in calculations, mathematical operations, or direct references to maintain context and functionality.

## How It Works

### 1. Dependency Detection
The system analyzes text for:
- **Mathematical Operations**: sum, add, calculate, compute
- **Direct References**: "call me at this phone", "verify this Aadhaar"
- **Calculations**: "what is the sum of X"

### 2. Preservation Logic
When PII data is found to be:
- Referenced in mathematical operations
- Directly mentioned multiple times
- Part of calculations or verifications

The system **preserves** the original data instead of anonymizing it.

## Examples

### ✅ PRESERVED (Dependencies Found)
```
Input: "My phone is 1234567890 and what is the sum of it?"
Output: "My phone is 1234567890 and what is the sum of it?"
Reason: Phone number referenced in mathematical context
```

```
Input: "My phone is 9876543210, call me at this phone 9876543210"
Output: "My phone is 9876543210, call me at this phone 9876543210"  
Reason: Direct reference to same phone number
```

### ❌ ANONYMIZED (No Dependencies)
```
Input: "My phone number is 9876543210 and I live in Mumbai"
Output: "My phone number is 942-335-1161x55940 and I live in New Roberttown"
Reason: No mathematical or direct references
```

## Supported Patterns

### Mathematical References
- "sum of [number]"
- "calculate [number]"
- "what is [number] + [number]"
- "total of [number]"

### Direct References  
- "my [type] is [number]"
- "call me at [number]"
- "verify this [number]"
- "contact [number]"

## Benefits

1. **Context Preservation** - Maintains meaning when data is functionally important
2. **Smart Detection** - Only preserves when truly necessary
3. **Flexible Patterns** - Handles various reference styles
4. **Consistent Logic** - Same rules apply across all PII types

The system now intelligently balances privacy protection with functional requirements!
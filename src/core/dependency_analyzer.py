import re
from typing import List, Dict, Set, Tuple, Any

class DependencyAnalyzer:
    def __init__(self):
        self.dependency_patterns = {
            'mathematical': [
                r'sum of ([\d\s-]+)',
                r'add ([\d\s-]+)',
                r'total of ([\d\s-]+)',
                r'addition of ([\d\s-]+)',
                r'([\d\s-]+) \+ ([\d\s-]+)',
                r'([\d\s-]+) - ([\d\s-]+)',
                r'([\d\s-]+) \* ([\d\s-]+)',
                r'([\d\s-]+) / ([\d\s-]+)',
                r'what is.*(?:sum|add|total|addition)\s+(?:of\s+)?([\d\s-]+)',
                r'tell me.*(?:sum|add|total|addition)\s+(?:of\s+)?([\d\s-]+)',
                r'calculate\s+(?:the\s+)?([\d\s-]+)',
                r'compute\s+(?:the\s+)?([\d\s-]+)',
            ],
            'reference': [
                r'my ([\w\s]+) is ([\d\s-]+)',
                r'the ([\w\s]+) ([\d\s-]+)',
                r'this ([\w\s]+) ([\d\s-]+)',
                r'that ([\w\s]+) ([\d\s-]+)',
                r'call.*at.*([\d\s-]+)',
                r'contact.*([\d\s-]+)',
                r'verify.*([\d\s-]+)',
                r'check.*([\d\s-]+)',
            ],
            'calculation': [
                r'what is.*(\d+)',
                r'tell me.*(\d+)',
                r'calculate.*(\d+)',
                r'result.*(\d+)',
            ]
        }
    
    def analyze_dependencies(self, text: str, entities: List[Any]) -> Dict[str, Set[str]]:
        """Analyze which PII entities are referenced in calculations or dependencies"""
        dependencies = {}
        text_lower = text.lower()
        
        # Find mathematical operations
        math_refs = self._find_mathematical_references(text_lower)
        
        # Find direct references
        direct_refs = self._find_direct_references(text_lower)
        
        # Map entities to their dependencies
        for entity in entities:
            entity_value = entity.text
            entity_key = f"{entity.label}:{entity_value}"
            
            # Check if this entity is referenced in math operations
            if self._is_referenced_in_math(entity_value, math_refs):
                dependencies[entity_key] = {'mathematical_dependency'}
            
            # Check if this entity is directly referenced
            if self._is_directly_referenced(entity_value, direct_refs):
                dependencies[entity_key] = dependencies.get(entity_key, set()) | {'direct_reference'}
        
        return dependencies
    
    def _find_mathematical_references(self, text: str) -> List[str]:
        """Find all numbers referenced in mathematical contexts"""
        math_numbers = []
        for pattern in self.dependency_patterns['mathematical']:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    math_numbers.extend(match)
                else:
                    math_numbers.append(match)
        return math_numbers
    
    def _find_direct_references(self, text: str) -> List[Tuple[str, str]]:
        """Find direct references like 'my phone is 123'"""
        references = []
        for pattern in self.dependency_patterns['reference']:
            matches = re.findall(pattern, text)
            references.extend(matches)
        return references
    
    def _is_referenced_in_math(self, entity_value: str, math_refs: List[str]) -> bool:
        """Check if entity value appears in mathematical operations"""
        # Extract digits from entity
        entity_digits = re.sub(r'\D', '', entity_value)
        
        for ref in math_refs:
            ref_digits = re.sub(r'\D', '', ref)
            if entity_digits == ref_digits:
                return True
        return False
    
    def _is_directly_referenced(self, entity_value: str, direct_refs: List[Tuple[str, str]]) -> bool:
        """Check if entity is directly referenced"""
        entity_digits = re.sub(r'\D', '', entity_value)
        
        for ref_item in direct_refs:
            if isinstance(ref_item, tuple) and len(ref_item) >= 2:
                ref_value = ref_item[1]
            else:
                ref_value = str(ref_item)
            
            ref_digits = re.sub(r'\D', '', ref_value)
            if entity_digits == ref_digits:
                return True
        return False
    
    def should_preserve_entity(self, entity: Any, text: str, dependencies: Dict[str, Set[str]]) -> bool:
        """Determine if entity should be preserved due to dependencies"""
        entity_key = f"{entity.label}:{entity.text}"
        
        # Always preserve medical conditions - they need solutions/information
        if entity.label == 'MEDICAL_CONDITION':
            return True
        
        # Preserve time references in medical contexts
        if entity.label == 'DATE' and self._is_medical_time_reference(entity.text, text):
            return True
        
        # Check if entity is in calculation context (this includes exclusion checks)
        if self._is_in_calculation_context(entity.text, text):
            return True
        
        # Only check dependencies if not excluded by calculation context
        if entity_key in dependencies:
            deps = dependencies[entity_key]
            # Only preserve mathematical dependencies, not direct references in assignment contexts
            if 'mathematical_dependency' in deps:
                return True
        
        return False
    
    def _is_in_calculation_context(self, entity_value: str, text: str) -> bool:
        """Check if entity appears in calculation context"""
        text_lower = text.lower()
        entity_lower = entity_value.lower()
        
        # First check for exclusion patterns - these indicate PII assignment/mention, not computation
        exclude_patterns = [
            # Personal information assignment
            rf'(?:my|his|her|their)\s+(?:name|phone|email|address|card|account|passport|pan|aadhaar|ssn)\s+(?:is|number is)\s+[\w\s@.-]*{re.escape(entity_lower)}',
            rf'(?:my|his|her|their)\s+(?:phone|mobile|contact)\s+(?:number\s+)?(?:is\s+)?{re.escape(entity_lower)}\b',
            rf'(?:phone|mobile|contact)\s+(?:number\s+)?(?:is\s+)?{re.escape(entity_lower)}\b',
            rf'(?:i|he|she|they)\s+(?:live|lives)\s+at\s+[\w\s,.-]*{re.escape(entity_lower)}',
            rf'(?:i|he|she|they)\s+(?:was|were)\s+born\s+on\s+[\w\s/-]*{re.escape(entity_lower)}',
            
            # Actions with PII (not computational)
            rf'(?:save|keep|store|share|send|forward|deliver|transfer)\s+[\w\s]*{re.escape(entity_lower)}',
            rf'{re.escape(entity_lower)}\s+(?:to|for|from)\s+\w+',
            rf'(?:applied|used|logged|admitted|drives|belongs)\s+[\w\s]*{re.escape(entity_lower)}',
            rf'{re.escape(entity_lower)}\s+(?:applied|used|logged|admitted|drives|belongs)',
            
            # Simple possession/ownership
            rf'(?:with|using)\s+[\w\s]*{re.escape(entity_lower)}',
            rf'{re.escape(entity_lower)}\s+(?:is|was|are|were)\s+(?:my|his|her|their)',
        ]
        
        # Computational patterns - these indicate the PII is being used for calculation/analysis
        computational_patterns = [
            # Mathematical operations with numbers
            rf'(?:add|sum|total|multiply|divide|subtract)\s+\d+\s+(?:to|and|with)\s+{re.escape(entity_lower)}',
            rf'(?:add|sum|total|multiply|divide|subtract)\s+{re.escape(entity_lower)}\s+(?:to|and|with)\s+\d+',
            rf'{re.escape(entity_lower)}\s*[\+\-\*\/×÷]\s*\d+',
            rf'\d+\s*[\+\-\*\/×÷]\s*{re.escape(entity_lower)}',
            
            # Counting and character analysis
            rf'count\s+(?:letters|characters|digits)\s+in\s+(?:the\s+name\s+)?{re.escape(entity_lower)}',
            rf'(?:how\s+many\s+)?(?:letters|characters|digits)\s+(?:are\s+)?(?:in\s+|before\s+@\s+in\s+)?{re.escape(entity_lower)}',
            rf'(?:length|size)\s+of\s+{re.escape(entity_lower)}',
            
            # Addition/calculation requests (more specific)
            rf'(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
            rf'{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\b',
            rf'(?:calculate|compute)\s+(?:the\s+)?(?:addition|sum|total)\s+(?:of\s+)?{re.escape(entity_lower)}\b',
            # Handle "calculate addition of my aadhaar number" where entity appears after the request
            rf'(?:calculate|compute|tell\s+me)\s+(?:the\s+)?(?:addition|sum|total)\s+of\s+(?:my\s+)?(?:aadhaar|phone|card|account)\s+(?:number\s+)?.*{re.escape(entity_lower)}',
            rf'{re.escape(entity_lower)}\s*(?:\+|plus)\s*\d+',
            rf'\d+\s*(?:\+|plus)\s*{re.escape(entity_lower)}',
            # Handle "number is X tell me addition of it" pattern
            rf'(?:number|phone|card)\s+is\s+{re.escape(entity_lower)}\s+(?:tell\s+me\s+)?(?:addition|sum|total)\s+(?:of\s+)?(?:it|this)',
            
            # Format validation and checking
            rf'check\s+if\s+{re.escape(entity_lower)}\s+(?:has|contains|follows|passes|is)',
            rf'(?:does\s+)?{re.escape(entity_lower)}\s+(?:have|contain|follow|pass|match)\s+(?:correct|\d+)',
            rf'(?:validate|verify)\s+{re.escape(entity_lower)}\s+(?:format|algorithm)',
            
            # Distance and location calculations
            rf'(?:find\s+)?distance\s+between\s+{re.escape(entity_lower)}\s+and',
            rf'distance\s+(?:from\s+)?{re.escape(entity_lower)}\s+to',
            
            # Age calculation from dates
            rf'calculate\s+(?:my\s+)?age\s+(?:from\s+)?(?:today\s+from\s+)?{re.escape(entity_lower)}',
            rf'(?:born\s+on\s+)?{re.escape(entity_lower)}[\s,]+calculate\s+(?:my\s+)?age',
            
            # Algorithm validation (Luhn, etc.)
            rf'{re.escape(entity_lower)}\s+(?:passes|using)\s+(?:the\s+)?luhn\s+algorithm',
            rf'(?:luhn\s+algorithm|passes)\s+(?:on\s+)?{re.escape(entity_lower)}',
            
            # Network/IP analysis
            rf'(?:is\s+)?{re.escape(entity_lower)}\s+(?:is\s+)?(?:a\s+)?(?:private|public)\s+ip\s+range',
            rf'check\s+if\s+{re.escape(entity_lower)}\s+is\s+(?:a\s+)?(?:private|public)',
        ]
        
        # Check if entity is referenced in computational context first (higher priority)
        for pattern in computational_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Check for exclusion patterns only if no computational context found
        for exclude_pattern in exclude_patterns:
            if re.search(exclude_pattern, text_lower):
                return False
        
        return False
    
    def _is_medical_info_request(self, entity_value: str, text: str) -> bool:
        """Check if medical condition is being asked about for informational purposes"""
        text_lower = text.lower()
        entity_lower = entity_value.lower()
        
        # Patterns indicating medical information requests
        medical_info_patterns = [
            rf'(?:i\s+have|diagnosed\s+with|suffering\s+from)\s+{re.escape(entity_lower)}.*(?:tell\s+me|what\s+to|how\s+to|advice|suggest)',
            rf'{re.escape(entity_lower)}.*(?:tell\s+me|what\s+to\s+eat|what\s+not\s+to\s+eat|diet|food|treatment|medicine)',
            rf'(?:with|having)\s+{re.escape(entity_lower)}.*(?:what\s+should|how\s+to|advice|recommend)',
            rf'(?:tell\s+me|advice|suggest|recommend).*(?:for|about)\s+{re.escape(entity_lower)}',
        ]
        
        for pattern in medical_info_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _is_medical_time_reference(self, entity_value: str, text: str) -> bool:
        """Check if date/time reference is in medical context"""
        text_lower = text.lower()
        entity_lower = entity_value.lower()
        
        # Medical time patterns
        medical_time_patterns = [
            rf'(?:diagnosed|treated|suffering|history).*{re.escape(entity_lower)}',
            rf'{re.escape(entity_lower)}.*(?:diagnosed|treated|suffering|ago)',
            rf'(?:since|for|during)\s+{re.escape(entity_lower)}',
        ]
        
        for pattern in medical_time_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
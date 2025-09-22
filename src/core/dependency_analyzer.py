import re
from typing import List, Dict, Set, Tuple, Any

class DependencyAnalyzer:
    def __init__(self):
        self.dependency_patterns = {
            'mathematical': [
                r'sum of ([\d\s-]+)',
                r'add ([\d\s-]+)',
                r'total of ([\d\s-]+)',
                r'([\d\s-]+) \+ ([\d\s-]+)',
                r'([\d\s-]+) - ([\d\s-]+)',
                r'([\d\s-]+) \* ([\d\s-]+)',
                r'([\d\s-]+) / ([\d\s-]+)',
                r'what is.*sum.*([\d\s-]+)',
                r'calculate.*([\d\s-]+)',
                r'compute.*([\d\s-]+)',
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
        
        if entity_key in dependencies:
            deps = dependencies[entity_key]
            # Preserve if it has mathematical or direct dependencies
            if 'mathematical_dependency' in deps or 'direct_reference' in deps:
                return True
        
        return False
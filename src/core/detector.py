import re
from dataclasses import dataclass
from typing import List
import logging

logger = logging.getLogger(__name__)

@dataclass
class PIIEntity:
    text: str
    label: str
    start: int
    end: int
    confidence: float = 0.95
    replacement: str = ""

class PIIDetector:
    """Detect PII using regex + optional spaCy NER."""
    def __init__(self, model_name: str = 'en_core_web_sm', config=None):
        self.config = config
        try:
            import spacy
            self.nlp = spacy.load(model_name)
            logger.info('spaCy loaded')
        except Exception:
            self.nlp = None
            logger.info('spaCy not available - regex-only detection')

        self.patterns = {
            # Email patterns
            'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
            
            # Phone patterns (international, Indian, US formats)
            'PHONE': re.compile(r'(?:\+91[\s-]?)?(?:\d{5}[\s-]?\d{5}|\d{4}[\s-]?\d{3}[\s-]?\d{3}|\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\d{10})\b'),
            
            # Indian Aadhaar number (12 digits)
            'AADHAAR': re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),
            
            # Indian PAN card (5 letters, 4 digits, 1 letter)
            'PAN': re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'),
            
            # Passport numbers (various formats)
            'PASSPORT': re.compile(r'\b[A-Z]\d{7}\b|\b[A-Z]{2}\d{6}\b|\b\d{9}\b'),
            
            # Driver's License (various formats)
            'DRIVING_LICENSE': re.compile(r'\b[A-Z]{2}\d{13}\b|\b[A-Z]\d{7}\b|\b\d{8,15}\b'),
            
            # Voter ID
            'VOTER_ID': re.compile(r'\b[A-Z]{3}\d{7}\b'),
            
            # Bank account numbers
            'BANK_ACCOUNT': re.compile(r'\b\d{9,18}\b'),
            
            # IFSC codes
            'IFSC': re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b'),
            
            # Credit/Debit card numbers
            'CREDIT_CARD': re.compile(r'\b(?:\d{4}[\s-]?){3}\d{4}\b'),
            
            # CVV numbers
            'CVV': re.compile(r'\bcvv[:\s]*\d{3,4}\b', re.IGNORECASE),
            
            # PIN codes
            'PIN_CODE': re.compile(r'\bpin[:\s]*\d{4,6}\b', re.IGNORECASE),
            
            # US SSN
            'SSN': re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            
            # IP addresses
            'IP_ADDRESS': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            
            # Dates (birth dates, etc.)
            'DATE': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'),
            
            # Age patterns
            'AGE': re.compile(r'\b(?:age|aged|years old)[:\s]*\d{1,3}\b|\b\d{1,3}\s*(?:years old|yrs old|y\.o\.)\b', re.IGNORECASE),
            
            # Address patterns
            'ADDRESS': re.compile(r'\b\d+[\s,]+[A-Za-z\s,.-]+(?:street|st|avenue|ave|road|rd|lane|ln|drive|dr|place|pl|court|ct)\b', re.IGNORECASE),
            
            # Medical record numbers
            'MEDICAL_ID': re.compile(r'\b(?:MRN|MR|medical record)[:\s#]*\d{6,12}\b', re.IGNORECASE),
            
            # Employee IDs
            'EMPLOYEE_ID': re.compile(r'\b(?:emp|employee|staff)[\s#:]*[A-Z0-9]{4,10}\b', re.IGNORECASE),
            
            # Student IDs
            'STUDENT_ID': re.compile(r'\b(?:student|roll)[\s#:]*[A-Z0-9]{4,10}\b', re.IGNORECASE),
            
            # Name patterns
            'NAME_PATTERN': re.compile(r'(?:my name is|i am|i\'m|call me|this is|here is|name:|i\'m called|they call me|known as|goes by|full name is|first name is|last name is|surname is|called|named)\s+([A-Za-z]+(?:[\s\-\']+[A-Za-z]+)*)', re.IGNORECASE),
            'STANDALONE_NAME': re.compile(r'\b([A-Z][a-z]+(?:[\s\-\']+[A-Z][a-z]+)+)\b'),
        }

        # small medical keywords to catch explicit health mentions (not exhaustive)
        self.medical_keywords = set(['diabetes','cancer','hypertension','asthma','covid','alzheimer','depression'])

    def detect_entities(self, text: str) -> List[PIIEntity]:
        if not text:
            return []
        entities = []

        # spaCy NER for PERSON/ORG/GPE/DATE if available
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ('PERSON','ORG','GPE','DATE'):
                        entities.append(PIIEntity(ent.text.strip(), ent.label_, ent.start_char, ent.end_char, 0.9))
            except Exception as e:
                logger.debug('spaCy error: %s', e)

        # regex matches
        for label, patt in self.patterns.items():
            if label == 'NAME_PATTERN':
                # Special handling for name patterns
                for m in patt.finditer(text):
                    name = m.group(1).strip()
                    if self._validate_name(name):
                        name_start = m.start(1)
                        name_end = m.end(1)
                        entities.append(PIIEntity(name, 'PERSON', name_start, name_end, 0.95))
            elif label == 'STANDALONE_NAME':
                # Standalone capitalized names (lower confidence)
                for m in patt.finditer(text):
                    name = m.group(1).strip()
                    if self._validate_standalone_name(name, text, m.start()):
                        entities.append(PIIEntity(name, 'PERSON', m.start(1), m.end(1), 0.85))
            else:
                for m in patt.finditer(text):
                    if self._validate(m.group(), label):
                        entities.append(PIIEntity(m.group().strip(), label, m.start(), m.end(), 0.98))

        # detect medical keywords as MEDICAL condition (word boundaries)
        low = text.lower()
        for kw in self.medical_keywords:
            import re
            for match in re.finditer(r'\b' + re.escape(kw) + r'\b', low):
                entities.append(PIIEntity(text[match.start():match.end()], 'MEDICAL_CONDITION', match.start(), match.end(), 0.9))

        # remove overlaps and duplicates
        entities = self._remove_overlaps(entities)
        return entities

    def _validate(self, txt: str, label: str) -> bool:
        if label == 'PHONE':
            digits = re.sub(r'\D','',txt)
            return 7 <= len(digits) <= 15
        elif label == 'AADHAAR':
            digits = re.sub(r'\D','',txt)
            return len(digits) == 12 and not digits.startswith(('0', '1'))
        elif label == 'PAN':
            return len(txt) == 10 and txt[:5].isalpha() and txt[5:9].isdigit() and txt[9].isalpha()
        elif label == 'PASSPORT':
            return 7 <= len(re.sub(r'\W','',txt)) <= 9
        elif label == 'DRIVING_LICENSE':
            clean = re.sub(r'\W','',txt)
            return 8 <= len(clean) <= 16
        elif label == 'VOTER_ID':
            return len(txt) == 10 and txt[:3].isalpha() and txt[3:].isdigit()
        elif label == 'BANK_ACCOUNT':
            digits = re.sub(r'\D','',txt)
            return 9 <= len(digits) <= 18
        elif label == 'IFSC':
            return len(txt) == 11 and txt[:4].isalpha() and txt[4] == '0'
        elif label == 'CREDIT_CARD':
            digits = re.sub(r'\D','',txt)
            return 13 <= len(digits) <= 19 and self._luhn_check(digits)
        elif label == 'CVV':
            digits = re.sub(r'\D','',txt)
            return 3 <= len(digits) <= 4
        elif label == 'PIN_CODE':
            digits = re.sub(r'\D','',txt)
            return 4 <= len(digits) <= 6
        elif label == 'SSN':
            digits = re.sub(r'\D','',txt)
            return len(digits) == 9
        elif label == 'IP_ADDRESS':
            parts = txt.split('.')
            if len(parts) != 4: return False
            try: return all(0 <= int(p) <= 255 for p in parts)
            except: return False
        elif label == 'AGE':
            age_num = re.search(r'\d+', txt)
            if age_num:
                age = int(age_num.group())
                return 1 <= age <= 120
            return False
        elif label in ['MEDICAL_ID', 'EMPLOYEE_ID', 'STUDENT_ID']:
            return len(re.sub(r'\W','',txt)) >= 4
        return True
    
    def _luhn_check(self, card_num: str) -> bool:
        """Validate credit card using Luhn algorithm"""
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        return luhn_checksum(card_num) == 0
    
    def _validate_name(self, name: str) -> bool:
        """Validate if a string looks like a person's name"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Check if it's all alphabetic (with spaces, hyphens, apostrophes)
        if not re.match(r'^[A-Za-z\s\-\']+$', name):
            return False
        
        # Check if it has reasonable length (2-50 chars)
        if not (2 <= len(name.strip()) <= 50):
            return False
        
        # Avoid common false positives
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'am', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        words = [w.lower() for w in name.split()]
        if any(w in common_words for w in words):
            return False
        
        return True
    
    def _validate_standalone_name(self, name: str, full_text: str, position: int) -> bool:
        """Validate standalone capitalized names with context"""
        if not self._validate_name(name):
            return False
        
        # Must have at least 2 words (first + last name)
        words = name.split()
        if len(words) < 2:
            return False
        
        # Avoid common false positives
        false_positives = {'New York', 'Los Angeles', 'San Francisco', 'United States', 'North America', 'South America', 'Middle East', 'New Delhi', 'Hong Kong', 'Saudi Arabia', 'Main Street', 'First Street', 'Second Street', 'Park Avenue', 'Wall Street'}
        if name in false_positives:
            return False
        
        # Check for street/place indicators
        street_words = {'street', 'avenue', 'road', 'boulevard', 'lane', 'drive', 'way', 'place', 'court', 'circle'}
        if any(word.lower() in street_words for word in words):
            return False
        
        # Check context for place indicators
        place_indicators = ['city', 'state', 'country', 'live in', 'visit', 'go to', 'located in', 'from']
        context_before = full_text[max(0, position-30):position].lower()
        context_after = full_text[position+len(name):position+len(name)+30].lower()
        
        if any(indicator in context_before or indicator in context_after for indicator in place_indicators):
            return False
        
        return True

    def _remove_overlaps(self, ents):
        if not ents: return ents
        
        # Remove exact duplicates first
        unique_ents = []
        seen = set()
        for e in ents:
            key = (e.start, e.end, e.label)
            if key not in seen:
                unique_ents.append(e)
                seen.add(key)
        
        if not unique_ents: return []
        
        # Sort by start position, then by length (longer first)
        unique_ents.sort(key=lambda e: (e.start, -(e.end - e.start)))
        
        result = []
        for current in unique_ents:
            # Check if current entity overlaps with any in result
            overlaps = False
            for existing in result:
                if (current.start < existing.end and current.end > existing.start):
                    # There's an overlap - keep the one with higher confidence or longer span
                    if (current.confidence > existing.confidence or 
                        (current.confidence == existing.confidence and 
                         (current.end - current.start) > (existing.end - existing.start))):
                        result.remove(existing)
                        result.append(current)
                    overlaps = True
                    break
            
            if not overlaps:
                result.append(current)
        
        return sorted(result, key=lambda e: e.start)

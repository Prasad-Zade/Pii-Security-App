import re
from dataclasses import dataclass
from typing import List
import logging
from .dependency_analyzer import DependencyAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class PIIEntity:
    text: str
    label: str
    start: int
    end: int
    confidence: float = 0.95
    replacement: str = ""
    preserve: bool = False

class ComprehensivePIIDetector:
    def __init__(self, model_name: str = 'en_core_web_sm', config=None):
        self.config = config
        self.dependency_analyzer = DependencyAnalyzer()
        try:
            import spacy
            self.nlp = spacy.load(model_name)
        except Exception:
            self.nlp = None

        self.patterns = {
            # Basic Identity
            'NAME_PATTERN': re.compile(r'(?:my name is|i am|i\'m|call me|this is|here is|name:|father\'s name|mother\'s name|spouse name|guardian name)\s+([A-Za-z]+(?:[\s\-\']+[A-Za-z]+)*)', re.IGNORECASE),
            'STANDALONE_NAME': re.compile(r'\b([A-Z][a-z]+(?:[\s\-\']+[A-Z][a-z]+)+)\b'),
            'GENDER': re.compile(r'\b(?:gender|sex):\s*(?:male|female|m|f|transgender|other)\b', re.IGNORECASE),
            'DOB': re.compile(r'\b(?:dob|date of birth|born on):\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', re.IGNORECASE),
            'AGE': re.compile(r'\b(?:age|aged|years old):\s*\d{1,3}\b|\b\d{1,3}\s*(?:years old|yrs old|y\.o\.)\b', re.IGNORECASE),
            'NATIONALITY': re.compile(r'\b(?:nationality|citizen of):\s*[A-Za-z\s]+\b', re.IGNORECASE),
            'RELIGION': re.compile(r'\b(?:religion):\s*(?:hindu|muslim|christian|sikh|buddhist|jain|parsi|other)\b', re.IGNORECASE),
            
            # Contact Information
            'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
            'PHONE': re.compile(r'(?:\+\d{1,3}[\s-]?)?(?:\d{5}[\s-]?\d{5}|\d{4}[\s-]?\d{3}[\s-]?\d{3}|\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\d{10})\b'),
            'ADDRESS': re.compile(r'\b\d+[\s,]+[A-Za-z\s,.-]+(?:street|st|avenue|ave|road|rd|lane|ln|drive|dr|place|pl|court|ct|nagar|colony|society)\b', re.IGNORECASE),
            'PIN_CODE': re.compile(r'\b(?:pin|zip|postal code):\s*\d{4,6}\b', re.IGNORECASE),
            'SOCIAL_MEDIA': re.compile(r'\b(?:@[A-Za-z0-9_]+|(?:twitter|instagram|linkedin|github|facebook)\.com/[A-Za-z0-9_]+)\b', re.IGNORECASE),
            
            # Government & Legal IDs
            'AADHAAR': re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'),
            'PAN': re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'),
            'PASSPORT': re.compile(r'\b[A-Z]\d{7}\b|\b[A-Z]{2}\d{6}\b|\b\d{9}\b'),
            'VOTER_ID': re.compile(r'\b[A-Z]{3}\d{7}\b'),
            'DRIVING_LICENSE': re.compile(r'\b[A-Z]{2}\d{13}\b|\b[A-Z]\d{7}\b'),
            'SSN': re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            'EMPLOYEE_ID': re.compile(r'\b(?:emp|employee|staff)[\s#:]*[A-Z0-9]{4,10}\b', re.IGNORECASE),
            'STUDENT_ID': re.compile(r'\b(?:student|roll|enrollment)[\s#:]*[A-Z0-9]{4,10}\b', re.IGNORECASE),
            
            # Financial Information
            'BANK_ACCOUNT': re.compile(r'\b(?:account|acc)[\s#:]*\d{9,18}\b', re.IGNORECASE),
            'CREDIT_CARD': re.compile(r'\b(?:\d{4}[\s-]?){3}\d{4}\b'),
            'CVV': re.compile(r'\bcvv:\s*\d{3,4}\b', re.IGNORECASE),
            'IFSC': re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b'),
            'UPI_ID': re.compile(r'\b[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\b'),
            'SALARY': re.compile(r'\b(?:salary|income):\s*(?:rs|₹|\$)?\s*\d+(?:,\d{3})*(?:\.\d{2})?\b', re.IGNORECASE),
            
            # Health & Biometric
            'BLOOD_GROUP': re.compile(r'\b(?:blood group|blood type):\s*(?:a|b|ab|o)[+-]?\b', re.IGNORECASE),
            'MEDICAL_RECORD': re.compile(r'\b(?:mrn|medical record|patient id)[\s#:]*[A-Z0-9]{6,12}\b', re.IGNORECASE),
            
            # Travel & Transport
            'VEHICLE_NUMBER': re.compile(r'\b[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}\b'),
            
            # Digital Identifiers
            'IP_ADDRESS': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'MAC_ADDRESS': re.compile(r'\b[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}\b'),
            'IMEI': re.compile(r'\b\d{15}\b'),
            
            # General patterns
            'DATE': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'),
        }

        self.medical_keywords = set(['diabetes','cancer','hypertension','asthma','covid','alzheimer','depression'])

    def detect_entities(self, text: str) -> List[PIIEntity]:
        if not text:
            return []
        entities = []

        # spaCy NER
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ('PERSON','ORG','GPE','DATE'):
                        entities.append(PIIEntity(ent.text.strip(), ent.label_, ent.start_char, ent.end_char, 0.9))
            except Exception as e:
                logger.debug('spaCy error: %s', e)

        # Regex patterns
        for label, patt in self.patterns.items():
            if label == 'NAME_PATTERN':
                for m in patt.finditer(text):
                    name = m.group(1).strip()
                    if self._validate_name(name):
                        entities.append(PIIEntity(name, 'PERSON', m.start(1), m.end(1), 0.95))
            elif label == 'STANDALONE_NAME':
                for m in patt.finditer(text):
                    name = m.group(1).strip()
                    if self._validate_standalone_name(name, text, m.start()):
                        entities.append(PIIEntity(name, 'PERSON', m.start(1), m.end(1), 0.85))
            else:
                for m in patt.finditer(text):
                    if self._validate(m.group(), label):
                        entities.append(PIIEntity(m.group().strip(), label, m.start(), m.end(), 0.98))

        # Medical keywords
        low = text.lower()
        for kw in self.medical_keywords:
            for match in re.finditer(r'\b' + re.escape(kw) + r'\b', low):
                entities.append(PIIEntity(text[match.start():match.end()], 'MEDICAL_CONDITION', match.start(), match.end(), 0.9))

        entities = self._remove_overlaps(entities)
        
        # Analyze dependencies and mark entities for preservation
        dependencies = self.dependency_analyzer.analyze_dependencies(text, entities)
        for entity in entities:
            if self.dependency_analyzer.should_preserve_entity(entity, text, dependencies):
                entity.preserve = True
        
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
        elif label == 'CREDIT_CARD':
            digits = re.sub(r'\D','',txt)
            return 13 <= len(digits) <= 19
        elif label == 'IP_ADDRESS':
            parts = txt.split('.')
            if len(parts) != 4: return False
            try: return all(0 <= int(p) <= 255 for p in parts)
            except: return False
        elif label == 'SSN':
            digits = re.sub(r'\D','',txt)
            return len(digits) == 9
        return True

    def _validate_name(self, name: str) -> bool:
        if not name or len(name.strip()) < 2:
            return False
        if not re.match(r'^[A-Za-z\s\-\']+$', name):
            return False
        if not (2 <= len(name.strip()) <= 50):
            return False
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'am', 'are'}
        words = [w.lower() for w in name.split()]
        if any(w in common_words for w in words):
            return False
        return True

    def _validate_standalone_name(self, name: str, full_text: str, position: int) -> bool:
        if not self._validate_name(name):
            return False
        words = name.split()
        if len(words) < 2:
            return False
        false_positives = {'New York', 'Los Angeles', 'San Francisco', 'United States', 'Main Street', 'First Street'}
        if name in false_positives:
            return False
        street_words = {'street', 'avenue', 'road', 'boulevard', 'lane', 'drive', 'way', 'place', 'court', 'circle'}
        if any(word.lower() in street_words for word in words):
            return False
        place_indicators = ['city', 'state', 'country', 'live in', 'visit', 'go to', 'located in', 'from']
        context_before = full_text[max(0, position-30):position].lower()
        context_after = full_text[position+len(name):position+len(name)+30].lower()
        if any(indicator in context_before or indicator in context_after for indicator in place_indicators):
            return False
        return True

    def _remove_overlaps(self, ents):
        if not ents: return ents
        unique_ents = []
        seen = set()
        for e in ents:
            key = (e.start, e.end, e.label)
            if key not in seen:
                unique_ents.append(e)
                seen.add(key)
        if not unique_ents: return []
        unique_ents.sort(key=lambda e: (e.start, -(e.end - e.start)))
        result = []
        for current in unique_ents:
            overlaps = False
            for existing in result:
                if (current.start < existing.end and current.end > existing.start):
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
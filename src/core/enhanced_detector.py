import re
from dataclasses import dataclass
from typing import List
import logging
try:
    from .ml_dependency_analyzer import MLDependencyAnalyzer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
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

class EnhancedPIIDetector:
    def __init__(self, model_name: str = 'en_core_web_sm'):
        if ML_AVAILABLE:
            self.dependency_analyzer = MLDependencyAnalyzer()
        else:
            self.dependency_analyzer = DependencyAnalyzer()
        try:
            import spacy
            self.nlp = spacy.load(model_name)
        except Exception:
            self.nlp = None

        # Comprehensive PII patterns for all categories
        self.patterns = {
            # Names and Identity
            'FULL_NAME': re.compile(r'\b(?:my name is|i am|i\'m|called|name:|full name)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+){1,2})(?=\s+[a-z]+)', re.IGNORECASE),
            'FIRST_NAME': re.compile(r'\b(?:first name|fname)\s*[:=]\s*([A-Z][a-z]+)', re.IGNORECASE),
            'LAST_NAME': re.compile(r'\b(?:last name|surname|lname)\s*[:=]\s*([A-Z][a-z]+)', re.IGNORECASE),
            'TITLE': re.compile(r'\b(?:Dr|Mr|Ms|Mrs|Prof|Sir|Madam)\.\s*[A-Z][a-z]+', re.IGNORECASE),
            'DOB': re.compile(r'\b(?:dob|date of birth|born on)\s*[:=]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', re.IGNORECASE),
            'AGE': re.compile(r'\b(?:age|aged)\s*[:=]?\s*(\d{1,3})\s*(?:years?|yrs?)?', re.IGNORECASE),
            'GENDER': re.compile(r'\b(?:gender|sex)\s*[:=]\s*(male|female|m|f|other)', re.IGNORECASE),
            'NATIONALITY': re.compile(r'\b(?:nationality|citizen)\s*[:=]\s*([A-Za-z\s]+)', re.IGNORECASE),
            'RELIGION': re.compile(r'\b(?:religion|religious)\s*[:=]\s*(hindu|muslim|christian|sikh|buddhist|jain|other)', re.IGNORECASE),
            'CASTE': re.compile(r'\b(?:caste|community|category)\s*[:=]\s*(general|obc|sc|st|ews|[A-Za-z\s]+)', re.IGNORECASE),
            
            # Family Relations
            'FATHER_NAME': re.compile(r'\b(?:father\'?s? name|father)\s*[:=]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', re.IGNORECASE),
            'MOTHER_NAME': re.compile(r'\b(?:mother\'?s? name|mother)\s*[:=]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', re.IGNORECASE),
            'SPOUSE_NAME': re.compile(r'\b(?:spouse|husband|wife)\s*[:=]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', re.IGNORECASE),
            
            # Contact Information
            'PHONE': re.compile(r'(?:\+\d{1,3}[\s-]?)?\d{10}|\(\d{3}\)\s*\d{3}[\s-]?\d{4}'),
            'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
            'ADDRESS': re.compile(r'\b\d+[,\s]+[A-Za-z\s,.-]+(?:street|st|avenue|ave|road|rd|lane|ln|nagar|colony)', re.IGNORECASE),
            'PIN_CODE': re.compile(r'\b(?:pin|zip|postal)\s*(?:code)?\s*[:=]?\s*(\d{4,6})\b', re.IGNORECASE),
            'SOCIAL_MEDIA': re.compile(r'(?:@\w+|(?:twitter|instagram|linkedin|github|facebook)\.com/\w+)', re.IGNORECASE),
            
            # Government IDs
            'AADHAAR': re.compile(r'\b(?:aadhaar|aadhar)\s*(?:no|number)?\s*[:=]?\s*(\d{4}[\s-]?\d{4}[\s-]?\d{4})', re.IGNORECASE),
            'PAN': re.compile(r'\b(?:pan)\s*(?:no|number|card)?\s*[:=]?\s*([A-Z]{5}\d{4}[A-Z])', re.IGNORECASE),
            'PASSPORT': re.compile(r'\b(?:passport)\s*(?:no|number)?\s*[:=]?\s*([A-Z]\d{7}|[A-Z]{2}\d{6})', re.IGNORECASE),
            'VOTER_ID': re.compile(r'\b(?:voter|election)\s*(?:id|card)\s*[:=]?\s*([A-Z]{3}\d{7})', re.IGNORECASE),
            'DRIVING_LICENSE': re.compile(r'\b(?:driving|dl)\s*(?:license|licence)\s*[:=]?\s*([A-Z]{2}\d{13})', re.IGNORECASE),
            'SSN': re.compile(r'\b(?:ssn|social security)\s*[:=]?\s*(\d{3}[-\s]?\d{2}[-\s]?\d{4})', re.IGNORECASE),
            'EMPLOYEE_ID': re.compile(r'\b(?:employee|emp|staff)\s*(?:id|number)\s*[:=]?\s*([A-Z0-9]{4,10})', re.IGNORECASE),
            'STUDENT_ID': re.compile(r'\b(?:student|roll|enrollment)\s*(?:id|no|number)\s*[:=]?\s*([A-Z0-9]{4,10})', re.IGNORECASE),
            
            # Financial Information
            'BANK_ACCOUNT': re.compile(r'\b(?:bank|account)\s*(?:no|number|a/c)\s*[:=]?\s*(\d{9,18})', re.IGNORECASE),
            'CREDIT_CARD': re.compile(r'\b(?:card|credit)\s*(?:no|number)?\s*[:=]?\s*(\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4})', re.IGNORECASE),
            'CVV': re.compile(r'\b(?:cvv|cvc)\s*[:=]?\s*(\d{3,4})', re.IGNORECASE),
            'IFSC': re.compile(r'\b(?:ifsc)\s*(?:code)?\s*[:=]?\s*([A-Z]{4}0[A-Z0-9]{6})', re.IGNORECASE),
            'UPI_ID': re.compile(r'\b(?:upi)\s*(?:id)?\s*[:=]?\s*([A-Za-z0-9._-]+@[A-Za-z0-9.-]+)', re.IGNORECASE),
            'SALARY': re.compile(r'\b(?:salary|income|ctc)\s*[:=]?\s*(?:rs|₹|\$)?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
            
            # Professional Details
            'OCCUPATION': re.compile(r'\b(?:occupation|job|work as|profession)\s*[:=]\s*([A-Za-z\s]+)', re.IGNORECASE),
            'EMPLOYER': re.compile(r'\b(?:employer|company|organization|work at)\s*[:=]?\s*([A-Za-z\s&.,]+)', re.IGNORECASE),
            'EXPERIENCE': re.compile(r'\b(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)', re.IGNORECASE),
            
            # Academic Information
            'UNIVERSITY': re.compile(r'\b(?:university|college|school|studied at)\s*[:=]?\s*([A-Za-z\s&.,]+)', re.IGNORECASE),
            'DEGREE': re.compile(r'\b(?:degree|qualification)\s*[:=]?\s*(b\.?tech|m\.?tech|mba|bca|mca|phd|bachelor|master)', re.IGNORECASE),
            'CGPA': re.compile(r'\b(?:cgpa|gpa|percentage|marks)\s*[:=]?\s*(\d+(?:\.\d+)?)', re.IGNORECASE),
            
            # Health Information
            'BLOOD_GROUP': re.compile(r'\b(?:blood group|blood type)\s*[:=]?\s*([ABO][\+\-]?)', re.IGNORECASE),
            'HEIGHT_WEIGHT': re.compile(r'\b(?:height|weight)\s*[:=]?\s*(\d+(?:\.\d+)?\s*(?:cm|kg|ft|lbs|inches)?)', re.IGNORECASE),
            'MEDICAL_ID': re.compile(r'\b(?:patient|medical|hospital)\s*(?:id|number)\s*[:=]?\s*([A-Z0-9]{6,12})', re.IGNORECASE),
            
            # Travel & Transport
            'VEHICLE_NUMBER': re.compile(r'\b(?:vehicle|car|bike)\s*(?:no|number)\s*[:=]?\s*([A-Z]{2}\d{2}[A-Z]{1,2}\d{4})', re.IGNORECASE),
            'FLIGHT_BOOKING': re.compile(r'\b(?:pnr|booking|flight)\s*(?:no|number)\s*[:=]?\s*([A-Z0-9]{6})', re.IGNORECASE),
            
            # Digital Identifiers
            'IP_ADDRESS': re.compile(r'\b(?:ip)\s*(?:address)?\s*[:=]?\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE),
            'MAC_ADDRESS': re.compile(r'\b(?:mac)\s*(?:address)?\s*[:=]?\s*([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})', re.IGNORECASE),
            'IMEI': re.compile(r'\b(?:imei)\s*[:=]?\s*(\d{15})', re.IGNORECASE),
            
            # Location Information
            'LOCATION': re.compile(r'\b(?:location|address|live in|from)\s*[:=]?\s*([A-Za-z\s,]+)', re.IGNORECASE),
            'HOMETOWN': re.compile(r'\b(?:hometown|native|birthplace)\s*[:=]?\s*([A-Za-z\s,]+)', re.IGNORECASE),
            
            # Standalone patterns for better detection
            'AADHAAR_STANDALONE': re.compile(r'\b(\d{4}\s+\d{4}\s+\d{4})\b'),
            'PAN_STANDALONE': re.compile(r'\b([A-Z]{5}\d{4}[A-Z])\b'),
            'PASSPORT_STANDALONE': re.compile(r'\b([A-Z]\d{7})\b'),
            'CREDIT_CARD_STANDALONE': re.compile(r'\b(\d{4}\s+\d{4}\s+\d{4}\s+\d{4})\b'),
            'VEHICLE_STANDALONE': re.compile(r'\b([A-Z]{2}\d{2}[A-Z]{1,2}\d{4})\b'),
            'MEDICAL_ID_STANDALONE': re.compile(r'\b(HOSP\d{6})\b'),
            
            # Sensitive Information
            'POLITICAL_PARTY': re.compile(r'\b(?:political|party|supports?)\s*[:=]?\s*([A-Za-z\s]+)', re.IGNORECASE),
            'CRIMINAL_RECORD': re.compile(r'\b(?:case|fir|criminal)\s*(?:no|number)\s*[:=]?\s*([A-Z0-9]{6,12})', re.IGNORECASE),
        }

    def detect_entities(self, text: str) -> List[PIIEntity]:
        if not text:
            return []
        
        entities = []
        
        # spaCy NER for general entities
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ('PERSON', 'ORG', 'GPE'):
                        entities.append(PIIEntity(ent.text.strip(), ent.label_, ent.start_char, ent.end_char, 0.9))
            except Exception as e:
                logger.debug('spaCy error: %s', e)
        
        # Pattern-based detection for specific PII types
        for label, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                if label in ['FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'FATHER_NAME', 'MOTHER_NAME', 'SPOUSE_NAME']:
                    # Extract name from capture group
                    name = match.group(1).strip()
                    if self._validate_name(name):
                        entities.append(PIIEntity(name, 'PERSON', match.start(1), match.end(1), 0.95))
                else:
                    # Extract the matched text or capture group
                    if match.groups():
                        matched_text = match.group(1).strip()
                        start_pos = match.start(1)
                        end_pos = match.end(1)
                    else:
                        matched_text = match.group(0).strip()
                        start_pos = match.start()
                        end_pos = match.end()
                    
                    if self._validate_entity(matched_text, label):
                        entities.append(PIIEntity(matched_text, label, start_pos, end_pos, 0.95))
        
        entities = self._remove_overlaps(entities)
        
        # Use ML or rule-based preservation
        if ML_AVAILABLE:
            for entity in entities:
                if self.dependency_analyzer.should_preserve_entity(entity, text):
                    entity.preserve = True
        else:
            dependencies = self.dependency_analyzer.analyze_dependencies(text, entities)
            for entity in entities:
                if self.dependency_analyzer.should_preserve_entity(entity, text, dependencies):
                    entity.preserve = True
        
        return entities
    
    def _validate_name(self, name: str) -> bool:
        if not name or len(name.strip()) < 2:
            return False
        if not re.match(r'^[A-Za-z\s\-\']+$', name):
            return False
        if len(name.strip()) > 50:
            return False
        
        # Avoid common false positives
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [w.lower() for w in name.split()]
        if any(w in common_words for w in words):
            return False
        
        return True
    
    def _validate_entity(self, text: str, label: str) -> bool:
        if not text or len(text.strip()) < 1:
            return False
        
        # Basic validation for different entity types
        if label in ['PHONE']:
            digits = re.sub(r'\D', '', text)
            return 7 <= len(digits) <= 15
        elif label in ['AADHAAR']:
            digits = re.sub(r'\D', '', text)
            return len(digits) == 12
        elif label in ['PAN']:
            return len(text) == 10 and text[:5].isalpha() and text[5:9].isdigit()
        elif label in ['EMAIL']:
            return '@' in text and '.' in text
        elif label in ['IP_ADDRESS']:
            parts = text.split('.')
            if len(parts) != 4:
                return False
            try:
                return all(0 <= int(p) <= 255 for p in parts)
            except:
                return False
        
        return True
    
    def _remove_overlaps(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        if not entities:
            return entities
        
        # Remove duplicates
        unique_entities = []
        seen = set()
        for entity in entities:
            key = (entity.start, entity.end, entity.label)
            if key not in seen:
                unique_entities.append(entity)
                seen.add(key)
        
        # Sort by start position and length
        unique_entities.sort(key=lambda e: (e.start, -(e.end - e.start)))
        
        # Remove overlaps, keeping higher confidence entities
        result = []
        for current in unique_entities:
            overlaps = False
            for existing in result:
                if (current.start < existing.end and current.end > existing.start):
                    if current.confidence > existing.confidence:
                        result.remove(existing)
                        result.append(current)
                    overlaps = True
                    break
            
            if not overlaps:
                result.append(current)
        
        return sorted(result, key=lambda e: e.start)
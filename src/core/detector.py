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
            'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
            'PHONE': re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'),
            'SSN': re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            'CREDIT_CARD': re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
            'IP_ADDRESS': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'DATE': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'),
            'MEDICAL_ID': re.compile(r'\bMD\d{6,12}\b', re.IGNORECASE),
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
                        entities.append(PIIEntity(ent.text, ent.label_, ent.start_char, ent.end_char, 0.9))
            except Exception as e:
                logger.debug('spaCy error: %s', e)

        # regex matches
        for label, patt in self.patterns.items():
            for m in patt.finditer(text):
                if self._validate(m.group(), label):
                    entities.append(PIIEntity(m.group(), label, m.start(), m.end(), 0.98))

        # detect medical keywords as MEDICAL condition (spanwise)
        low = text.lower()
        for kw in self.medical_keywords:
            idx = low.find(kw)
            if idx != -1:
                entities.append(PIIEntity(text[idx:idx+len(kw)], 'MEDICAL_CONDITION', idx, idx+len(kw), 0.9))

        # remove overlaps, prefer longer spans
        entities = self._remove_overlaps(entities)
        return entities

    def _validate(self, txt: str, label: str) -> bool:
        if label == 'PHONE':
            digits = re.sub(r'\D','',txt)
            return 7 <= len(digits) <= 15
        if label == 'SSN':
            digits = re.sub(r'\D','',txt); return len(digits)==9
        if label == 'CREDIT_CARD':
            digits = re.sub(r'\D','',txt); return 13 <= len(digits) <= 19
        if label == 'IP_ADDRESS':
            parts = txt.split('.')
            if len(parts)!=4: return False
            try: return all(0<=int(p)<=255 for p in parts)
            except: return False
        return True

    def _remove_overlaps(self, ents):
        if not ents: return ents
        ents.sort(key=lambda e:(e.start, -e.end))
        out = []
        cur = ents[0]
        for e in ents[1:]:
            if e.start < cur.end:
                if (e.end - e.start) > (cur.end - cur.start):
                    cur = e
            else:
                out.append(cur); cur = e
        out.append(cur)
        return out

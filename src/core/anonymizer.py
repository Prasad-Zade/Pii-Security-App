from faker import Faker
import logging
import csv
import random
from typing import List, Tuple, Dict, Optional
from .detector import PIIEntity

logger = logging.getLogger(__name__)

class AnonymizationEngine:
    def __init__(self, locale='en_US', seed=42, config=None, csv_data_path=None):
        self.config = config
        self.faker = Faker(locale)
        Faker_seed = seed
        try:
            Faker.seed(Faker_seed)
        except Exception:
            pass
        self.replacement_cache = {}
        self._replacement_sources = {}
        
        # CSV data support
        self._csv_data = {}
        self._has_csv_data = False
        if csv_data_path:
            self._load_csv_data(csv_data_path)
        
        self.strategies = {
            'PERSON': self._name,
            'ORG': self._org,
            'GPE': self._location,
            'EMAIL': self._email,
            'PHONE': self._phone,
            'SSN': self._ssn,
            'CREDIT_CARD': self._cc,
            'IP_ADDRESS': self._ip,
            'DATE': self._date,
            'MEDICAL_ID': self._medical_id,
            'MEDICAL_CONDITION': self._medical_cond
        }

    def _load_csv_data(self, csv_path: str):
        """Load replacement data from CSV file"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    for key, value in row.items():
                        if key not in self._csv_data:
                            self._csv_data[key] = []
                        if value and value.strip():  # Only add non-empty values
                            self._csv_data[key].append(value.strip())
            
            self._has_csv_data = len(self._csv_data) > 0
            if self._has_csv_data:
                logger.info(f"Loaded CSV data with {len(self._csv_data)} categories")
            
        except Exception as e:
            logger.warning(f"Failed to load CSV data from {csv_path}: {e}")
            self._has_csv_data = False

    def set_csv_data(self, csv_data: Dict[str, List[str]]):
        """Set CSV data directly from a dictionary"""
        self._csv_data = csv_data
        self._has_csv_data = len(csv_data) > 0

    def _get_replacement_data(self, category: str, original_value: str) -> Tuple[str, str]:
        """Get replacement data from CSV, return (replacement, source)"""
        if not self._has_csv_data or category not in self._csv_data:
            return None, 'faker'
        
        # Get a random replacement from the CSV data
        replacements = self._csv_data[category]
        if not replacements:
            return None, 'faker'
        
        # Use consistent replacement for same original value
        random.seed(hash(original_value))
        replacement = random.choice(replacements)
        random.seed()  # Reset seed
        
        return replacement, 'csv'

    def anonymize_text(self, text: str, entities: List[PIIEntity]) -> Tuple[str, Dict[str,str]]:
        if not entities: return text, {}
        # process from end to start to keep indices valid
        ents = sorted(entities, key=lambda e: e.start, reverse=True)
        out = text
        mapping = {}
        for e in ents:
            rep = self._generate(e)
            e.replacement = rep
            out = out[:e.start] + rep + out[e.end:]
            mapping[rep] = e.text
            print(entities)
            print (mapping)
        return out, mapping

    def _generate(self, e: PIIEntity) -> str:
        key = f"{e.label}::{e.text.strip().lower()}"
        if key in self.replacement_cache:
            return self.replacement_cache[key]
        fn = self.strategies.get(e.label, lambda s:'['+e.label+']')
        rep = fn(e.text)
        self.replacement_cache[key] = rep
        return rep

    def _name(self, orig):
        # Check if CSV data is available first
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('name', orig)
            if replacement:
                self._replacement_sources['name'] = source
                return self._preserve_title(orig, replacement)
        
        # Fallback to Faker
        self._replacement_sources['name'] = 'faker'
        return self._preserve_title(orig, self.faker.name())

    def _preserve_title(self, orig: str, replacement: str) -> str:
        """Preserve title if present in original name"""
        low = orig.lower()
        title = ''
        if low.startswith('dr.') or low.startswith('dr '): title='Dr. '
        elif low.startswith('mr.') or low.startswith('mr '): title='Mr. '
        elif low.startswith('ms.') or low.startswith('ms '): title='Ms. '
        elif low.startswith('mrs.') or low.startswith('mrs '): title='Mrs. '
        
        return title + replacement

    def _org(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('organization', orig)
            if replacement:
                self._replacement_sources['organization'] = source
                return replacement
        
        self._replacement_sources['organization'] = 'faker'
        return self.faker.company()

    def _location(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('location', orig)
            if replacement:
                self._replacement_sources['location'] = source
                return replacement
        
        self._replacement_sources['location'] = 'faker'
        return self.faker.city()

    def _email(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('email', orig)
            if replacement:
                self._replacement_sources['email'] = source
                return replacement
        
        # Faker fallback with domain preservation
        self._replacement_sources['email'] = 'faker'
        try:
            domain = orig.split('@')[1]
            if 'gmail' in domain.lower(): 
                return f"{self.faker.user_name()}@gmail.com"
        except Exception: 
            pass
        return self.faker.email()

    def _phone(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('phone', orig)
            if replacement:
                self._replacement_sources['phone'] = source
                return replacement
        
        self._replacement_sources['phone'] = 'faker'
        return self.faker.phone_number()

    def _ssn(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('ssn', orig)
            if replacement:
                self._replacement_sources['ssn'] = source
                return replacement
        
        self._replacement_sources['ssn'] = 'faker'
        return self.faker.ssn()

    def _cc(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('credit_card', orig)
            if replacement:
                self._replacement_sources['credit_card'] = source
                return replacement
        
        self._replacement_sources['credit_card'] = 'faker'
        return self.faker.credit_card_number()

    def _ip(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('ip_address', orig)
            if replacement:
                self._replacement_sources['ip_address'] = source
                return replacement
        
        self._replacement_sources['ip_address'] = 'faker'
        return self.faker.ipv4()

    def _date(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('date', orig)
            if replacement:
                self._replacement_sources['date'] = source
                return replacement
        
        self._replacement_sources['date'] = 'faker'
        return self.faker.date()

    def _medical_id(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('medical_id', orig)
            if replacement:
                self._replacement_sources['medical_id'] = source
                return replacement
        
        self._replacement_sources['medical_id'] = 'faker'
        return 'MD'+str(self.faker.random_number(digits=8))

    def _medical_cond(self, orig):
        if self._has_csv_data:
            replacement, source = self._get_replacement_data('medical_condition', orig)
            if replacement:
                self._replacement_sources['medical_condition'] = source
                return replacement
        
        self._replacement_sources['medical_condition'] = 'faker'
        return '[medical_condition]'

    def get_replacement_sources(self) -> Dict[str, str]:
        """Get information about the sources used for replacements"""
        return self._replacement_sources.copy()

    def get_csv_categories(self) -> List[str]:
        """Get available categories in the loaded CSV data"""
        return list(self._csv_data.keys()) if self._has_csv_data else []
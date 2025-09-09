from faker import Faker
import logging
import random
from typing import List, Tuple, Dict
from .comprehensive_detector import PIIEntity

logger = logging.getLogger(__name__)

class ComprehensiveAnonymizer:
    def __init__(self, locale='en_US', seed=42):
        self.faker = Faker(locale)
        self.seed = seed
        Faker.seed(seed)
        random.seed(seed)
        self.replacement_cache = {}

        self.strategies = {
            # Basic Identity
            'PERSON': self._name, 'NAME_PATTERN': self._name, 'STANDALONE_NAME': self._name,
            'GENDER': self._gender, 'DOB': self._dob, 'AGE': self._age,
            'NATIONALITY': self._nationality, 'RELIGION': self._religion,
            
            # Contact
            'EMAIL': self._email, 'PHONE': self._phone, 'ADDRESS': self._address,
            'PIN_CODE': self._pin_code, 'SOCIAL_MEDIA': self._social_media,
            
            # Government IDs
            'AADHAAR': self._aadhaar, 'PAN': self._pan, 'PASSPORT': self._passport,
            'VOTER_ID': self._voter_id, 'DRIVING_LICENSE': self._driving_license,
            'SSN': self._ssn, 'EMPLOYEE_ID': self._employee_id, 'STUDENT_ID': self._student_id,
            
            # Financial
            'BANK_ACCOUNT': self._bank_account, 'CREDIT_CARD': self._cc, 'CVV': self._cvv,
            'IFSC': self._ifsc, 'UPI_ID': self._upi_id, 'SALARY': self._salary,
            
            # Health
            'BLOOD_GROUP': self._blood_group, 'MEDICAL_RECORD': self._medical_record,
            'MEDICAL_CONDITION': self._medical_cond,
            
            # Travel
            'VEHICLE_NUMBER': self._vehicle_number,
            
            # Digital
            'IP_ADDRESS': self._ip, 'MAC_ADDRESS': self._mac_address, 'IMEI': self._imei,
            
            # General
            'ORG': self._org, 'GPE': self._location, 'DATE': self._date,
        }

    def anonymize_text(self, text: str, entities: List[PIIEntity]) -> Tuple[str, Dict[str,str]]:
        if not entities: return text, {}
        entities = self._validate_entities(entities)
        ents = sorted(entities, key=lambda e: e.start, reverse=True)
        out = text
        mapping = {}
        
        for e in ents:
            if hasattr(e, 'preserve') and e.preserve:
                # Skip anonymization for preserved entities
                continue
            
            rep = self._generate(e)
            e.replacement = rep
            original_text = text[e.start:e.end]
            out = out[:e.start] + rep + out[e.end:]
            mapping[rep] = original_text
            
        return out, mapping

    def _generate(self, e: PIIEntity) -> str:
        key = f"{e.label}::{e.text.strip().lower()}"
        if key in self.replacement_cache:
            return self.replacement_cache[key]
        
        original_seed = random.getstate()
        random.seed(hash(e.text.strip().lower()) + self.seed)
        
        fn = self.strategies.get(e.label, lambda s: f'[{e.label}]')
        rep = fn(e.text)
        
        random.setstate(original_seed)
        self.replacement_cache[key] = rep
        return rep

    def _validate_entities(self, entities: List[PIIEntity]) -> List[PIIEntity]:
        if not entities: return entities
        sorted_entities = sorted(entities, key=lambda e: e.start)
        validated = []
        for entity in sorted_entities:
            overlaps = False
            for existing in validated:
                if (entity.start < existing.end and entity.end > existing.start):
                    overlaps = True
                    break
            if not overlaps:
                validated.append(entity)
        return validated

    # Anonymization methods
    def _name(self, orig): return self.faker.name()
    def _gender(self, orig): return 'gender: other'
    def _dob(self, orig): return f"dob: {self.faker.date()}"
    def _age(self, orig): 
        age = self.faker.random_int(min=18, max=80)
        if 'years old' in orig.lower(): return f"{age} years old"
        elif 'aged' in orig.lower(): return f"aged {age}"
        else: return f"age: {age}"
    def _nationality(self, orig): return f"nationality: {self.faker.country()}"
    def _religion(self, orig): return 'religion: other'
    
    def _email(self, orig):
        try:
            domain = orig.split('@')[1]
            if 'gmail' in domain.lower(): return f"{self.faker.user_name()}@gmail.com"
        except: pass
        return self.faker.email()
    def _phone(self, orig): return self.faker.phone_number()
    def _address(self, orig): return self.faker.address().replace('\n', ', ')
    def _pin_code(self, orig): return f"pin: {self.faker.random_number(digits=6)}"
    def _social_media(self, orig): return f"@{self.faker.user_name()}"
    
    def _aadhaar(self, orig): return f"{self.faker.random_number(digits=4)} {self.faker.random_number(digits=4)} {self.faker.random_number(digits=4)}"
    def _pan(self, orig):
        letters1 = ''.join(self.faker.random_letters(length=5)).upper()
        digits = self.faker.random_number(digits=4)
        letter2 = self.faker.random_letter().upper()
        return f"{letters1}{digits:04d}{letter2}"
    def _passport(self, orig):
        if len(orig) == 8 and orig[0].isalpha():
            return self.faker.random_letter().upper() + str(self.faker.random_number(digits=7))
        return str(self.faker.random_number(digits=9))
    def _voter_id(self, orig):
        letters = ''.join(self.faker.random_letters(length=3)).upper()
        return f"{letters}{self.faker.random_number(digits=7)}"
    def _driving_license(self, orig): return f"{self.faker.state_abbr()}{self.faker.random_number(digits=13)}"
    def _ssn(self, orig): return self.faker.ssn()
    def _employee_id(self, orig): return f"EMP{self.faker.random_number(digits=6)}"
    def _student_id(self, orig): return f"STU{self.faker.random_number(digits=6)}"
    
    def _bank_account(self, orig): return str(self.faker.random_number(digits=12))
    def _cc(self, orig): return self.faker.credit_card_number()
    def _cvv(self, orig): return f"cvv: {self.faker.random_number(digits=3)}"
    def _ifsc(self, orig):
        bank_code = ''.join(self.faker.random_letters(length=4)).upper()
        branch_code = ''.join(self.faker.random_letters(length=6)).upper()
        return f"{bank_code}0{branch_code}"
    def _upi_id(self, orig): return f"{self.faker.user_name()}@paytm"
    def _salary(self, orig): return f"salary: Rs.{self.faker.random_number(digits=6)}"
    
    def _blood_group(self, orig): return f"blood group: {self.faker.random_element(['A+', 'B+', 'AB+', 'O+'])}"
    def _medical_record(self, orig): return f"MRN{self.faker.random_number(digits=8)}"
    def _medical_cond(self, orig): return '[medical_condition]'
    
    def _vehicle_number(self, orig): return f"{self.faker.state_abbr()}{self.faker.random_number(digits=2)}{self.faker.random_letters(length=2).upper()}{self.faker.random_number(digits=4)}"
    
    def _ip(self, orig): return self.faker.ipv4()
    def _mac_address(self, orig): return ':'.join([f"{self.faker.random_int(min=0, max=255):02x}" for _ in range(6)])
    def _imei(self, orig): return str(self.faker.random_number(digits=15))
    
    def _org(self, orig): return self.faker.company()
    def _location(self, orig): return self.faker.city()
    def _date(self, orig): return self.faker.date()
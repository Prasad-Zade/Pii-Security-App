#!/usr/bin/env python3

import json
import random
from faker import Faker
from typing import List, Dict, Tuple
import re

class PIIDatasetGenerator:
    def __init__(self):
        self.fake = Faker(['en_IN', 'en_US'])
        
    def generate_training_data(self, num_samples: int = 1000) -> List[Dict]:
        """Generate training data with labels"""
        dataset = []
        
        for _ in range(num_samples):
            scenario_type = random.choice([
                'name_only', 'contact_info', 'government_ids', 
                'mixed_context', 'computational_context', 'medical_context'
            ])
            
            sample = self._generate_scenario(scenario_type)
            dataset.append(sample)
            
        return dataset
    
    def _generate_scenario(self, scenario_type: str) -> Dict:
        if scenario_type in ['name_only', 'contact_info', 'government_ids', 'medical_context']:
            return self._generate_mixed_scenario()
        elif scenario_type == 'mixed_context':
            return self._generate_mixed_scenario()
        elif scenario_type == 'computational_context':
            return self._generate_computational_scenario()
    
    def _generate_computational_scenario(self) -> Dict:
        """Generate scenarios where PII should be preserved for computation"""
        name = self.fake.first_name()
        phone = f"{random.randint(1000000000,9999999999)}"
        aadhaar = f"{random.randint(1000,9999)}{random.randint(1000,9999)}{random.randint(1000,9999)}"
        
        templates = [
            f"My name is {name}, calculate the addition of my phone number {phone}",
            f"I am {name}, tell me the sum of digits in {aadhaar}",
            f"My Aadhaar is {aadhaar}, calculate its digit sum",
            f"Phone number {phone}, find the addition of all digits",
            f"I am {name} and my phone is {phone}, tell me addition of it"
        ]
        text = random.choice(templates)
        
        entities = []
        
        if name in text:
            entities.append({
                'text': name,
                'label': 'PERSON',
                'start': text.find(name),
                'end': text.find(name) + len(name),
                'should_preserve': False
            })
        
        if phone in text:
            entities.append({
                'text': phone,
                'label': 'PHONE',
                'start': text.find(phone),
                'end': text.find(phone) + len(phone),
                'should_preserve': True
            })
            
        if aadhaar in text:
            entities.append({
                'text': aadhaar,
                'label': 'AADHAAR',
                'start': text.find(aadhaar),
                'end': text.find(aadhaar) + len(aadhaar),
                'should_preserve': True
            })
            
        return {'text': text, 'entities': entities}
    
    def _generate_mixed_scenario(self) -> Dict:
        name = self.fake.name()
        phone = f"{random.randint(1000000000,9999999999)}"
        
        templates = [
            f"I am {name} and my phone number is {phone}, tell me addition of it",
            f"My name is {name}, calculate sum of my phone {phone}"
        ]
        text = random.choice(templates)
        
        entities = []
        
        if name in text:
            entities.append({
                'text': name,
                'label': 'PERSON',
                'start': text.find(name),
                'end': text.find(name) + len(name),
                'should_preserve': False
            })
        
        if phone in text:
            entities.append({
                'text': phone,
                'label': 'PHONE',
                'start': text.find(phone),
                'end': text.find(phone) + len(phone),
                'should_preserve': True
            })
            
        return {'text': text, 'entities': entities}

def generate_datasets():
    generator = PIIDatasetGenerator()
    
    train_data = generator.generate_training_data(800)
    test_data = generator.generate_training_data(200)
    
    with open('d:/BE Project Claude/training/training_data.json', 'w') as f:
        json.dump(train_data, f, indent=2)
    
    with open('d:/BE Project Claude/training/test_data.json', 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"Generated {len(train_data)} training samples")
    print(f"Generated {len(test_data)} test samples")
    
    return train_data, test_data

if __name__ == "__main__":
    generate_datasets()
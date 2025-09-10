#!/usr/bin/env python3

import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
from typing import List, Dict, Tuple

class PIIModelTrainer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def extract_features(self, text: str, entity: Dict) -> Dict:
        """Extract features for preservation decision"""
        features = {}
        
        # Text context features
        text_lower = text.lower()
        entity_text = entity['text'].lower()
        
        # Mathematical context
        features['has_calculate'] = 'calculate' in text_lower
        features['has_addition'] = 'addition' in text_lower or 'sum' in text_lower
        features['has_count'] = 'count' in text_lower
        features['has_tell_me'] = 'tell me' in text_lower
        
        # Entity type features
        features['is_person'] = entity['label'] == 'PERSON'
        features['is_phone'] = entity['label'] == 'PHONE'
        features['is_aadhaar'] = entity['label'] == 'AADHAAR'
        features['is_medical'] = entity['label'] == 'MEDICAL_CONDITION'
        
        # Position features
        entity_pos = text_lower.find(entity_text)
        features['entity_position'] = entity_pos / len(text) if len(text) > 0 else 0
        
        # Context window features
        window_size = 50
        start_window = max(0, entity_pos - window_size)
        end_window = min(len(text), entity_pos + len(entity_text) + window_size)
        context = text_lower[start_window:end_window]
        
        features['context_has_my'] = 'my' in context
        features['context_has_is'] = ' is ' in context
        features['context_has_number'] = 'number' in context
        
        return features
    
    def prepare_training_data(self, dataset: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features and labels for training"""
        X = []
        y = []
        
        for sample in dataset:
            text = sample['text']
            for entity in sample['entities']:
                features = self.extract_features(text, entity)
                feature_vector = [
                    features['has_calculate'],
                    features['has_addition'],
                    features['has_count'],
                    features['has_tell_me'],
                    features['is_person'],
                    features['is_phone'],
                    features['is_aadhaar'],
                    features['is_medical'],
                    features['entity_position'],
                    features['context_has_my'],
                    features['context_has_is'],
                    features['context_has_number']
                ]
                
                X.append(feature_vector)
                y.append(1 if entity['should_preserve'] else 0)
        
        return np.array(X), np.array(y)
    
    def train(self, train_data: List[Dict], test_data: List[Dict]):
        """Train the model"""
        print("Preparing training data...")
        X_train, y_train = self.prepare_training_data(train_data)
        
        print("Preparing test data...")
        X_test, y_test = self.prepare_training_data(test_data)
        
        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")
        print(f"Preserve ratio in training: {np.mean(y_train):.2f}")
        
        # Train the model
        print("Training model...")
        self.classifier.fit(X_train, y_train)
        
        # Evaluate
        print("Evaluating model...")
        train_score = self.classifier.score(X_train, y_train)
        test_score = self.classifier.score(X_test, y_test)
        
        print(f"Training accuracy: {train_score:.3f}")
        print(f"Test accuracy: {test_score:.3f}")
        
        # Predictions
        y_pred = self.classifier.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Anonymize', 'Preserve']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        feature_names = [
            'has_calculate', 'has_addition', 'has_count', 'has_tell_me',
            'is_person', 'is_phone', 'is_aadhaar', 'is_medical',
            'entity_position', 'context_has_my', 'context_has_is', 'context_has_number'
        ]
        
        importances = self.classifier.feature_importances_
        print("\nFeature Importance:")
        for name, importance in zip(feature_names, importances):
            print(f"{name}: {importance:.3f}")
    
    def predict_preserve(self, text: str, entity: Dict) -> bool:
        """Predict if entity should be preserved"""
        features = self.extract_features(text, entity)
        feature_vector = np.array([[
            features['has_calculate'],
            features['has_addition'],
            features['has_count'],
            features['has_tell_me'],
            features['is_person'],
            features['is_phone'],
            features['is_aadhaar'],
            features['is_medical'],
            features['entity_position'],
            features['context_has_my'],
            features['context_has_is'],
            features['context_has_number']
        ]])
        
        return bool(self.classifier.predict(feature_vector)[0])
    
    def save_model(self, filepath: str):
        """Save trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'classifier': self.classifier,
                'vectorizer': self.vectorizer
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.classifier = data['classifier']
            self.vectorizer = data['vectorizer']
        print(f"Model loaded from {filepath}")

def main():
    # Load datasets
    with open('d:/BE Project Claude/training/training_data.json', 'r') as f:
        train_data = json.load(f)
    
    with open('d:/BE Project Claude/training/test_data.json', 'r') as f:
        test_data = json.load(f)
    
    # Train model
    trainer = PIIModelTrainer()
    trainer.train(train_data, test_data)
    
    # Save model
    trainer.save_model('d:/BE Project Claude/training/pii_model.pkl')
    
    # Test with Lokesh case
    print("\n" + "="*50)
    print("Testing with Lokesh case:")
    
    test_text = "i am lokesh sutar i want you to calculate the addition of my aadhaar number aadhaar : 765297568120"
    
    # Test entities
    test_entities = [
        {'text': 'lokesh sutar', 'label': 'PERSON'},
        {'text': '765297568120', 'label': 'AADHAAR'}
    ]
    
    for entity in test_entities:
        should_preserve = trainer.predict_preserve(test_text, entity)
        print(f"Entity: {entity['text']} ({entity['label']}) -> {'PRESERVE' if should_preserve else 'ANONYMIZE'}")

if __name__ == "__main__":
    main()
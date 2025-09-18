import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load the Excel dataset and prepare it for training"""
    try:
        # Load the Excel file
        df = pd.read_excel('tests/functional_dependency_dataset.xlsx')
        print(f"Dataset loaded successfully with {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        
        # Display first few rows
        print("\nFirst 5 rows:")
        print(df.head())
        
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def preprocess_data(df):
    """Preprocess the data for machine learning"""
    # Create features from text columns
    df['text_features'] = df['Input'].fillna('') + ' ' + df['Masked'].fillna('')
    
    # Create target variable based on functional dependency
    if 'Functional_Dependency' in df.columns:
        # Use existing functional dependency column
        df['target'] = df['Functional_Dependency'].map({'High': 1, 'Low': 0})
    else:
        # Create target based on whether input and masked are different
        df['target'] = (df['Input'] != df['Masked']).astype(int)
    
    # Remove rows with missing targets
    df = df.dropna(subset=['target'])
    
    print(f"\nTarget distribution:")
    print(df['target'].value_counts())
    
    return df

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and evaluate them"""
    
    # Vectorize text features
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*50}")
        print(f"Training {name}")
        print(f"{'='*50}")
        
        # Train the model
        model.fit(X_train_vec, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_vec)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        
        print(f"\nDetailed Classification Report:")
        print(classification_report(y_test, y_pred))
        
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
    
    return results

def main():
    print("PII Security Model Training")
    print("="*50)
    
    # Load data
    df = load_and_prepare_data()
    if df is None:
        return
    
    # Preprocess data
    df = preprocess_data(df)
    
    if len(df) == 0:
        print("No valid data found for training")
        return
    
    # Prepare features and target
    X = df['text_features']
    y = df['target']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train and evaluate models
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Summary
    print(f"\n{'='*50}")
    print("FINAL RESULTS SUMMARY")
    print(f"{'='*50}")
    
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")

if __name__ == "__main__":
    main()
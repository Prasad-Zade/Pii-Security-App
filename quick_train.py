import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Load data
df = pd.read_excel('tests/functional_dependency_dataset.xlsx')
df['features'] = df['Input'] + ' ' + df['Masked']
df['target'] = df['Functional_Dependency'].map({'High': 1, 'Low': 0})

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['features'], df['target'], test_size=0.2, random_state=42)

# Vectorize and train
vectorizer = TfidfVectorizer(max_features=500)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train_vec, y_train)

# Predict and evaluate
y_pred = model.predict(X_test_vec)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred, average='weighted'):.4f}")
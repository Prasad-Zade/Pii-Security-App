import requests
import json

API_KEY = "AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo"

# Test different model combinations
models_to_test = [
    ("v1beta", "gemini-pro"),
    ("v1beta", "gemini-1.5-pro"),
    ("v1beta", "gemini-1.5-flash"),
    ("v1beta", "gemini-1.5-pro-latest"),
    ("v1beta", "gemini-1.5-flash-latest"),
    ("v1", "gemini-pro"),
    ("v1", "gemini-1.5-pro"),
    ("v1", "gemini-1.5-flash"),
]

def test_model(version, model_name):
    url = f"https://generativelanguage.googleapis.com/v{version}/models/{model_name}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, how are you?"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"OK {version}/{model_name}: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data:
                print(f"  Response: {data['candidates'][0]['content']['parts'][0]['text'][:50]}...")
                return True
        else:
            print(f"  Error: {response.text[:100]}...")
    except Exception as e:
        print(f"FAIL {version}/{model_name}: {str(e)[:50]}...")
    
    return False

print("Testing Gemini API models...")
working_models = []

for version, model in models_to_test:
    if test_model(version, model):
        working_models.append((version, model))

print(f"\nWorking models: {working_models}")
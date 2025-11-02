import requests
import json

API_KEY = "AIzaSyDJb2LPaNY5TVAYCpYmAnNnv0vQcLplQyE"

# Test different Gemini endpoints
endpoints = [
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}",
    f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}",
]

payload = {
    "contents": [{
        "parts": [{"text": "What is a ball?"}]
    }]
}

for i, url in enumerate(endpoints):
    print(f"\nTesting endpoint {i+1}: {url.split('/')[-1].split('?')[0]}")
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data:
                print(f"SUCCESS: {data['candidates'][0]['content']['parts'][0]['text'][:100]}...")
                break
        else:
            print(f"Error: {response.text[:200]}...")
    except Exception as e:
        print(f"Exception: {e}")

print("\nTest complete.")
import google.generativeai as genai

genai.configure(api_key="AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo")

print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")

# Test with the most basic model
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello")
    print(f"Success with gemini-pro: {response.text}")
except Exception as e:
    print(f"gemini-pro failed: {e}")

try:
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content("Hello")
    print(f"Success with models/gemini-pro: {response.text}")
except Exception as e:
    print(f"models/gemini-pro failed: {e}")
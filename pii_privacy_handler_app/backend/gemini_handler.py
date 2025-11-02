"""
Gemini LLM Handler for generating intelligent responses
"""

import google.generativeai as genai

class GeminiHandler:
    def __init__(self):
        genai.configure(api_key="AIzaSyAJpAxoKWc9biprobj_KXP0hxCRoByAEFo")
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_response(self, masked_query: str, context: str = "General") -> str:
        """Generate response using Gemini API"""
        try:
            prompt = f"You are a helpful AI assistant. The user's personal information has been masked for privacy. Respond naturally and helpfully to: {masked_query}"
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.7
                )
            )
            
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini API error: {e}")
            return "I understand your message. How can I help you further?"
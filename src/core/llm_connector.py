import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiConnector:
    def __init__(self, api_key=None, model="gemini-2.0-flash-exp"):  # Updated to a more stable model
        # Use API key from argument, environment, or hardcoded fallback
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "AIzaSyCkc83znIV2wqNeV53llqdQU5slPcvCu9U"
        self.model_name = model
        self.available = False
        self.model = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.available = True
                logger.info(f"Gemini client ready with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to init Gemini: {e}")
        else:
            logger.warning("No API key found for Gemini.")

    def is_available(self):
        return self.available and self.model is not None

    def generate(self, prompt, max_tokens=1000, temperature=0.7):
        if not self.is_available():
            return self._mock(prompt)

        try:
            from google.generativeai import types
            
            # Configure safety settings to be less restrictive for PII detection
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config=types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                ),
                safety_settings=safety_settings
            )

            # Handle different response scenarios
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                
                # Check finish reason
                finish_reason = getattr(candidate, 'finish_reason', None)
                finish_reason_name = getattr(finish_reason, 'name', str(finish_reason))
                
                if finish_reason_name == 'SAFETY':
                    logger.warning("Content blocked by safety filters")
                    return "⚠ Content was blocked by safety filters. This may happen with PII-related content."
                
                elif finish_reason_name == 'RECITATION':
                    logger.warning("Content blocked due to recitation")
                    return "⚠ Content blocked due to recitation concerns."
                
                elif finish_reason_name not in ['STOP', 'MAX_TOKENS']:
                    logger.warning(f"Unexpected finish reason: {finish_reason_name}")
                    return f"⚠ Generation stopped unexpectedly: {finish_reason_name}"
                
                # Try to extract text content
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        texts = []
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                texts.append(part.text)
                        
                        if texts:
                            return "\n".join(texts).strip()
                
                # Fallback: try the quick accessor if available
                if hasattr(response, 'text') and response.text:
                    return response.text.strip()
            
            # If we get here, no valid content was found
            logger.warning("No valid content found in response")
            return "⚠ No valid response generated."

        except Exception as e:
            logger.warning(f"LLM call failed: {e}")
            return self._mock(prompt)

    def _mock(self, prompt):
        """Fallback responses when API is unavailable"""
        canned = [
            "Thank you — processed anonymously.",
            "I have reviewed the text and can help.",
            "Analysis complete - privacy concerns noted.",
            "Content processed with privacy considerations."
        ]
        return canned[hash(prompt) % len(canned)]

    def test_connection(self):
        """Test the connection with a simple prompt"""
        if not self.is_available():
            return False, "API not available"
        
        try:
            test_response = self.generate("Say 'Hello, I am working correctly!'", max_tokens=1000, temperature=0.7)
            if "working correctly" in test_response.lower():
                return True, "Connection successful"
            else:
                return False, f"Unexpected response: {test_response}"
        except Exception as e:
            return False, f"Test failed: {e}"
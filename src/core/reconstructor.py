from typing import Dict
import re

class ReconstructionModule:
    def reconstruct(self, text: str, mapping: Dict[str, str]) -> str:
        if not text or not mapping:
            return text
        
        out = text
        # Sort by length (longest first) to avoid partial replacements
        sorted_mapping = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
        
        for anon_token, original_value in sorted_mapping:
            if anon_token in out:
                # Use word boundary matching for better accuracy
                # But fallback to simple replace if word boundaries don't work
                try:
                    # Try word boundary replacement first
                    pattern = r'\b' + re.escape(anon_token) + r'\b'
                    if re.search(pattern, out):
                        out = re.sub(pattern, original_value, out)
                    else:
                        # Fallback to simple replacement
                        out = out.replace(anon_token, original_value)
                except:
                    # If regex fails, use simple replacement
                    out = out.replace(anon_token, original_value)
        
        return out

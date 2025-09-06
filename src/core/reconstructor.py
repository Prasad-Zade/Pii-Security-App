from typing import Dict
class ReconstructionModule:
    def reconstruct(self, text: str, mapping: Dict[str,str]) -> str:
        if not text or not mapping: return text
        out = text
        # replace anonymized tokens with original values (longest first)
        for anon, orig in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
            out = out.replace(anon, orig)
        return out

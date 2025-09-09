from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import time, json
from .comprehensive_detector import ComprehensivePIIDetector, PIIEntity
from .comprehensive_anonymizer import ComprehensiveAnonymizer
from .llm_connector import GeminiConnector
from .reconstructor import ReconstructionModule

@dataclass
class ProcessingResult:
    original_text: str
    anonymized_text: str
    llm_response: str
    reconstructed_text: str
    entities: List[PIIEntity]
    processing_time: float
    privacy_score: float

class PIIPrivacySystem:
    def __init__(self, config_path='config.yaml'):
        self.detector = ComprehensivePIIDetector()
        self.anonymizer = ComprehensiveAnonymizer()
        self.llm = GeminiConnector()
        self.reconstructor = ReconstructionModule()
        self.history = []

    def process(self, text: str, include_llm: bool = True):
        start = time.time()
        
        # Ensure text is properly cleaned
        text = text.strip() if text else ''
        if not text:
            return ProcessingResult('', '', '', '', [], 0.0, 100.0)
        
        try:
            # Detect entities
            ents = self.detector.detect_entities(text)
            
            # Anonymize text
            anon, mapping = self.anonymizer.anonymize_text(text, ents)
            
            # Generate LLM response if requested
            llm_resp = ''
            if include_llm and anon:
                llm_resp = self.llm.generate(anon)
            
            # Reconstruct text
            reconstructed = ''
            if llm_resp and mapping:
                reconstructed = self.reconstructor.reconstruct(llm_resp, mapping)
            
            pt = time.time() - start
            score = self._calc_score(ents, text)
            
            res = ProcessingResult(text, anon, llm_resp, reconstructed, ents, pt, score)
            self.history.append(res)
            return res
            
        except Exception as e:
            # Return error result
            pt = time.time() - start
            return ProcessingResult(text, f'[ERROR: {str(e)}]', '', '', [], pt, 0.0)

    def _calc_score(self, ents, txt):
        if not ents: return 100.0
        total = len(txt) or 1
        weight = sum(len(e.text) for e in ents)/total
        return round(max(0, 100 - weight*100),2)

    def process_csv(self, csv_path, text_column='text', include_llm=False):
        import pandas as pd
        df = pd.read_csv(csv_path)
        results = []
        for idx, row in df.iterrows():
            text = str(row.get(text_column,'') )
            res = self.process(text, include_llm=include_llm)
            results.append({'original':res.original_text,'anonymized':res.anonymized_text,'llm':res.llm_response,'reconstructed':res.reconstructed_text})
        out_df = pd.DataFrame(results)
        out_path = csv_path.replace('.csv','_processed.csv')
        out_df.to_csv(out_path,index=False)
        return out_path

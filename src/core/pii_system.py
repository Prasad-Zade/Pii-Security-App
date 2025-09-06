from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import time, json
from .detector import PIIDetector, PIIEntity
from .anonymizer import AnonymizationEngine
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
        self.detector = PIIDetector()
        self.anonymizer = AnonymizationEngine()
        self.llm = GeminiConnector()
        self.reconstructor = ReconstructionModule()
        self.history = []

    def process(self, text:str, include_llm:bool=True):
        start = time.time()
        ents = self.detector.detect_entities(text)
        anon, mapping = self.anonymizer.anonymize_text(text, ents)
        llm_resp = ''
        if include_llm:
            llm_resp = self.llm.generate(anon)
        reconstructed = self.reconstructor.reconstruct(llm_resp, mapping) if llm_resp else ''
        pt = time.time()-start
        score = self._calc_score(ents, text)
        res = ProcessingResult(text, anon, llm_resp, reconstructed, ents, pt, score)
        self.history.append(res)
        return res

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

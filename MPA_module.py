from typing import Dict, Tuple, List
from monitoring import CitationMonitor
from plan import CitationVerifier
from act import CitationAct
from api_openai import OpenAIClient
from review import CitationRefiner
import time

class SelfHealingLayer:
    """
    Modulo integrato per monitorare, verificare e correggere citazioni DOI.
    (Monitor → Plan → Act) così da fare una pipeline che integra i 3 moduli
    """
    def __init__(self):
        self.monitor = CitationMonitor()
        self.verifier = CitationVerifier()
        self.act = CitationAct()
        self.client = OpenAIClient()
        self.refiner = CitationRefiner(self.client)

    def process_text(self, text: str) -> Dict[str, any]:
        start_total = time.time()
        # === MONITORING ===
        dois = self.monitor.extract_dois(text)
        print(f"DOI trovati: {dois}")

        # === PLANNING ===
        verification_results = {}
        for doi in dois:
            is_valid, metadata = self.verifier.verify_doi(doi)
            verification_results[doi] = (is_valid, metadata)

        # === ACT ===
        adapted_text = self.act.adapt_text(text, verification_results)

        # === REVIEW ===
        has_invalid_dois = any(not result[0] for result in verification_results.values())

        refined_sentence_text = adapted_text
        refined_full_text = adapted_text
        metrics_sentence = {}
        metrics_full = {}

        if has_invalid_dois:
            print("\n--- Avvio doppia revisione (testo intero vs frasi mirate) ---")
            refined_sentence_text, metrics_sentence = self.refiner.refine_text(adapted_text)
            refined_full_text, metrics_full = self.refiner.refine_full_text(adapted_text)
        total_time = time.time() - start_total
        
        # === OUTPUT ===
        return {
            "num_dois": len(dois),
            "num_invalid_dois": sum(not r[0] for r in verification_results.values()),
            "original_text": text,
            "adapted_text": adapted_text,
            "refined_text_sentence_based": refined_sentence_text,
            "refined_text_full": refined_full_text,
            "verification_results": verification_results,
            "stats": self.verifier.get_stats(),
            "metrics_sentence": metrics_sentence,
            "metrics_full": metrics_full,
            "total_time": total_time,
        }


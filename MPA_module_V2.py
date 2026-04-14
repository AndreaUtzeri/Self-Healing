import time
from typing import Dict, Any, List

from monitor_V2 import CitationMonitorLLM
from plan_V2 import CitationPlanSimple
from act_V2 import CitationAct
from citation_verifier_V2 import CitationVerifier
from review import CitationRefiner
from api_openai import OpenAIClient


class SelfHealingLayerV2:
    """
    Complete pipeline:
    MONITOR → PLAN → ACT → REVIEW
    Updated version using the new LLM-based modules.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAIClient(model=model)

        self.monitor = CitationMonitorLLM(self.client)
        self.verifier = CitationVerifier()
        self.plan = CitationPlanSimple(self.verifier)
        self.act = CitationAct()
        self.refiner = CitationRefiner(self.client)

    def process_text(self, text: str) -> Dict[str, Any]:
        start_total = time.time()

        
        # 1. MONITORING → Citation detection
        
        monitor_output: List[Dict] = self.monitor.extract_references(text)

        
        # 2. PLAN → Crossref verification
        
        plan_output: Dict[str, Dict] = self.plan.run(monitor_output)

        
        # 3. ACT → Correct / Remove / Mark
       
        adapted_text = self.act.apply(text, plan_output)

        
        # 4. REVIEW → Correct only sentences with omission placeholders
        
        refined_sentence_text, review_stats = self.refiner.refine_text(adapted_text)

        total_time = time.time() - start_total

        
        # OUTPUT
       
        return {
            "original_text": text,
            "monitor_output": monitor_output,
            "plan_output": plan_output,
            "adapted_text": adapted_text,
            "refined_sentence_text": refined_sentence_text,
            "metrics_sentence": review_stats,
            "total_time": total_time
        }
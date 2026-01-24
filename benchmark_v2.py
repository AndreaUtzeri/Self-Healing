import json
from collections import defaultdict
from data_test_generator import TEST_REFERENCES
from plan_V2 import CitationPlanSimple
from citation_verifier_V2 import CitationVerifier
import re

class CitationBenchmarkTestRefs:
    def __init__(self):
        self.verifier = CitationVerifier()
        self.plan = CitationPlanSimple(self.verifier)
        self.references = TEST_REFERENCES

    def parse_reference(self, detected_form):
        """Parsing semplice per test."""
        doi, authors, year, title, venue = None, None, None, None, None

        if "DOI:" in detected_form:
            doi = detected_form.split("DOI:")[1].strip().rstrip(".")
        year_match = re.search(r"\((\d{4})\)", detected_form)
        if year_match:
            year = int(year_match.group(1))
        author_match = re.match(r"^(.*?)\(", detected_form)
        if author_match:
            authors_str = author_match.group(1)
            authors = [a.strip().split()[0] for a in authors_str.split(",")]
        title_match = re.search(r"\)\. (.*?)\. ", detected_form)
        if title_match:
            title = title_match.group(1)
        venue_match = re.findall(r"\. (.*?)\. DOI:", detected_form)
        if venue_match:
            venue = venue_match[-1]

        return {
            "doi": doi,
            "authors": authors,
            "year": year,
            "title": title,
            "venue": venue
        }

    def run_single_test(self):
        """Applica il plan su tutti i riferimenti e restituisce i risultati."""
        plan_output = {}
        for idx, ref_data in enumerate(self.references):
            ref_id = f"ref_{idx+1}"
            detected_form = ref_data["text"]
            ground_label = ref_data["label"]

            parsed = self.parse_reference(detected_form)
            verification = self.plan.verify_reference({"parsed": parsed})

            plan_output[ref_id] = {
                "detected_form": detected_form,
                "parsed": parsed,
                "verification": verification,
                "expected_label": ground_label
            }
        return plan_output

    def run_benchmark(self):
        plan_output = self.run_single_test()
        confusion = defaultdict(int)
        taxonomy = defaultdict(int)

        for ref_id, ref in plan_output.items():
            status = ref["verification"]["status"]
            expected = ref["expected_label"]

            taxonomy[status] += 1

            if expected == "partial":
                confusion["UNVERIFIABLE"] += 1
                continue

            if expected == "true":
                if status == "verified":
                    confusion["TP"] += 1
                else:
                    confusion["FN"] += 1
            elif expected == "corrupt":
                if status in ["metadata_mismatch", "invalid_doi"]:
                    confusion["TN"] += 1
                elif status == "verified":
                    confusion["FP"] += 1

        TP = confusion["TP"]
        TN = confusion["TN"]
        FP = confusion["FP"]
        FN = confusion["FN"]
        UNVERIFIABLE = confusion["UNVERIFIABLE"]

        total_decidable = TP + TN + FP + FN
        accuracy = (TP + TN) / total_decidable if total_decidable else 0.0
        precision = TP / (TP + FP) if (TP + FP) else 0.0
        recall = TP / (TP + FN) if (TP + FN) else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0

        summary = {
            "confusion_matrix": {
                "TP": TP,
                "FN": FN,
                "TN": TN,
                "UNVERIFIABLE": UNVERIFIABLE,
                "FP": FP
            },
            "taxonomy": dict(taxonomy),
            "metrics": {
                "decidable_references": total_decidable,
                "accuracy": round(accuracy, 2),
                "precision": round(precision, 2),
                "recall": round(recall, 2),
                "f1": round(f1, 2)
            }
        }

        print(json.dumps(summary, indent=2))
        return summary


if __name__ == "__main__":
    benchmark = CitationBenchmarkTestRefs()
    benchmark.run_benchmark()

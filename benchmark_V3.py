import json
import statistics
from collections import defaultdict
from typing import List, Dict

from data_test_generator_V2 import generate_test_references
from plan_V2 import CitationPlanSimple
from citation_verifier_V2 import CitationVerifier


# =============================================================================
# BENCHMARK
# =============================================================================
class CitationBenchmarkV3:

    SEEDS = [42, 123, 256, 789, 1001]
    N_PER_RUN = 50

    def __init__(self):
        self.verifier = CitationVerifier()
        self.plan = CitationPlanSimple(self.verifier)

    # ------------------------------------------------------------------
    # SINGLE RUN
    # ------------------------------------------------------------------
    def _run_single(self, references: List[Dict]) -> Dict:

        confusion = defaultdict(int)
        taxonomy = defaultdict(int)

        label_counts = {"true": 0, "corrupt": 0, "partial": 0}

        partial_total = 0
        partial_as_verified = 0

        for ref_data in references:

            parsed = ref_data["parsed"]
            label = ref_data["label"]

            verification = self.plan.verify_reference({"parsed": parsed})
            status = verification["status"]

            taxonomy[status] += 1
            label_counts[label] += 1

            # ----------------------------------------------------------
            # PARTIAL (not evaluable cases)
            # ----------------------------------------------------------
            if label == "partial":
                partial_total += 1
                if status == "verified":
                    partial_as_verified += 1
                continue

            # ----------------------------------------------------------
            # TRUE vs CORRUPT
            # ----------------------------------------------------------
            if label == "true":
                if status == "verified":
                    confusion["TP"] += 1
                else:
                    confusion["FN"] += 1

            elif label == "corrupt":

                # TN = only explicit contradictions
                if status == "metadata_mismatch":
                    confusion["TN"] += 1
                elif status == "invalid_doi":
                    confusion["TN"] += 1

                # FP = critical error (accepting corrupted citation)
                elif status == "verified":
                    confusion["FP"] += 1

        TP = confusion["TP"]
        TN = confusion["TN"]
        FP = confusion["FP"]
        FN = confusion["FN"]

        total = TP + TN + FP + FN

        accuracy  = (TP + TN) / total if total else 0.0
        precision = TP / (TP + FP) if (TP + FP) else 0.0
        recall    = TP / (TP + FN) if (TP + FN) else 0.0
        f1        = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0

        return {
            "confusion_matrix": {
                "TP": TP,
                "TN": TN,
                "FP": FP,
                "FN": FN,
                "UNVERIFIABLE": partial_total
            },
            "metrics": {
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4)
            },
            "partial_analysis": {
                "partial_total": partial_total,
                "partial_as_verified": partial_as_verified,
                "partial_fp_rate": (
                    partial_as_verified / partial_total
                    if partial_total else 0.0
                )
            },
            "taxonomy": dict(taxonomy),
            "label_counts": label_counts
        }

    # ------------------------------------------------------------------
    # AGGREGATION
    # ------------------------------------------------------------------
    @staticmethod
    def _aggregate(run_results: List[Dict]) -> Dict:

        metric_keys = ["accuracy", "precision", "recall", "f1"]
        aggregated = {}

        for k in metric_keys:
            vals = [r["metrics"][k] for r in run_results]
            aggregated[k] = {
                "mean": round(statistics.mean(vals), 4),
                "stdev": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
                "min": min(vals),
                "max": max(vals)
            }

        cm_keys = ["TP", "TN", "FP", "FN", "UNVERIFIABLE"]
        cm_mean = {}

        for k in cm_keys:
            vals = [r["confusion_matrix"][k] for r in run_results]
            cm_mean[k] = round(statistics.mean(vals), 2)

        return {
            "metrics": aggregated,
            "confusion_matrix_mean": cm_mean
        }

    # ------------------------------------------------------------------
    # RUN BENCHMARK
    # ------------------------------------------------------------------
    def run_benchmark(self, verbose: bool = True):

        results = {}

        for mode, apply_degradation in [("optimistic", False), ("degraded", True)]:

            if verbose:
                print(f"\n{'='*60}")
                print(f" MODE: {mode.upper()}")
                print(f"{'='*60}")

            run_results = []

            for seed in self.SEEDS:

                refs = generate_test_references(
                    n=self.N_PER_RUN,
                    seed=seed,
                    apply_degradation=apply_degradation
                )

                single = self._run_single(refs)
                run_results.append(single)

                if verbose:
                    m = single["metrics"]
                    print(
                        f"[seed={seed}] "
                        f"acc={m['accuracy']:.3f} "
                        f"prec={m['precision']:.3f} "
                        f"rec={m['recall']:.3f} "
                        f"f1={m['f1']:.3f}"
                    )

            agg = self._aggregate(run_results)

            results[mode] = {
                "per_run": run_results,
                "aggregated": agg
            }

            if verbose:
                print("\n--- AGGREGATED ---")
                print(json.dumps(agg, indent=2))

        return results


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":

    print("=" * 60)
    print(" CitationPlan Benchmark V3")
    print(" Evidence-based verification (no missing-field penalty)")
    print("=" * 60)

    benchmark = CitationBenchmarkV3()
    results = benchmark.run_benchmark(verbose=True)

    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved: benchmark_results.json")
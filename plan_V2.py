import re
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher


class CitationPlanSimple:
    def __init__(self, verifier, title_threshold: float = 0.97):
        self.verifier = verifier
        self.title_threshold = title_threshold

    # --------------------------
    # Normalization (lowercase, punctuation removal, whitespace ...)
    # --------------------------
    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _extract_last_names(self, authors: List[str]) -> List[str]:
        last_names = []
        for a in authors:
            tokens = self._normalize_text(a).split()
            if tokens:
                last_names.append(tokens[-1])
        return last_names

    # --------------------------
    # asymmetric author matching
    # --------------------------
    def _compare_authors(
        self, authors_ref: List[str], authors_meta: List[str]
    ) -> bool:
        """
        If the parser extracted fewer authors than Crossref (et_al case),
        verify that ALL extracted authors appear in Crossref.
        No false positives: a fabricated author will never be in Crossref.

        If the counts are similar, use a symmetric ratio >= 0.97.
        """
        if not authors_ref or not authors_meta:
            return False

        ref_last  = self._extract_last_names(authors_ref)
        meta_last = self._extract_last_names(authors_meta)

        if not ref_last or not meta_last:
            return False

        ref_set  = set(ref_last)
        meta_set = set(meta_last)
        matches  = len(ref_set & meta_set)

        # et_al case: parser extracted significantly fewer authors than Crossref
        # Conservative condition: all extracted authors must match
        if len(ref_set) <= len(meta_set) * 0.6:
            return matches == len(ref_set)   # all present in Crossref

        # Normal case: symmetric ratio (high threshold)
        ratio = matches / max(len(ref_set), len(meta_set))
        return ratio >= 0.97

    # --------------------------
    # title matching with truncation handling
    # --------------------------
    def _compare_title(
        self, title_ref: Optional[str], title_meta: Optional[str]
    ) -> bool:
        """
        If the extracted title is much shorter than the Crossref one
        (truncated_title case), use a normalized prefix check.
        Otherwise, use fuzzy ratio >= 0.97.
        """
        if not title_ref or not title_meta:
            return False

        t_ref  = self._normalize_text(title_ref)
        t_meta = self._normalize_text(title_meta)

        # Truncated title case: reference much shorter than metadata
        if len(t_ref) < len(t_meta) * 0.65:
            # Extracted title must be a prefix of metadata
            return t_meta.startswith(t_ref) and len(t_ref) >= 15

        ratio = SequenceMatcher(None, t_ref, t_meta).ratio()
        return ratio >= self.title_threshold

    # --------------------------
    # zero contradictions on available fields
    # --------------------------
    def verify_reference(self, ref: Dict) -> Dict:
        parsed = ref["parsed"]

        doi    = parsed.get("doi")
        authors = parsed.get("authors")
        year   = parsed.get("year")
        title  = parsed.get("title")

        if not doi:
            return {
                "status": "insufficient_metadata",
                "reason": "Missing DOI → cannot safely verify",
                "crossref_matches": []
            }

        valid, crossref_meta = self.verifier.verify_doi(doi)

        if not valid:
            return {
                "status": "invalid_doi",
                "reason": "DOI not found in Crossref",
                "crossref_metadata": None
            }

        # --- Check only fields actually extracted by the parser ---
        checks: List[Tuple[str, bool]] = []

        if authors:   # None or empty list → skip
            checks.append(("authors", self._compare_authors(
                authors, crossref_meta.get("authors", [])
            )))
        if year:      # None → skip (missing_year degradation)
            checks.append(("year", year == crossref_meta.get("year")))
        if title:     # None → skip (missing_title degradation)
            checks.append(("title", self._compare_title(
                title, crossref_meta.get("title")
            )))

        # No fields available: valid DOI but nothing to compare
        if not checks:
            return {
                "status": "doi_only_verified",
                "reason": "DOI valid but no metadata to cross-check",
                "crossref_metadata": crossref_meta
            }

        # Explicit contradiction on at least one field → reject
        contradictions = [name for name, ok in checks if not ok]
        if contradictions:
            return {
                "status": "metadata_mismatch",
                "contradicted_fields": contradictions,
                "author_match": dict(checks).get("authors"),
                "year_match":   dict(checks).get("year"),
                "title_match":  dict(checks).get("title"),
                "crossref_metadata": crossref_meta
            }

        # All available fields match Crossref
        return {
            "status": "verified",
            "checked_fields": [name for name, _ in checks],
            "author_match": dict(checks).get("authors"),
            "year_match":   dict(checks).get("year"),
            "title_match":  dict(checks).get("title"),
            "crossref_metadata": crossref_meta
        }

    # --------------------------
    # Main
    # --------------------------
    def run(self, monitor_output: List[Dict]) -> Dict:
        results = {}
        for ref in monitor_output:
            ref_id = ref["id"]
            verification = self.verify_reference(ref)
            results[ref_id] = {
                "detected_form": ref["detected_form"],
                "parsed": ref["parsed"],
                "verification": verification
            }
        return results
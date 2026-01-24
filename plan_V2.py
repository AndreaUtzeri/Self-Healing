from typing import Dict, List, Optional
from difflib import SequenceMatcher

class CitationPlanSimple:
    def __init__(self, verifier, title_threshold: float = 0.85):
        self.verifier = verifier
        self.title_threshold = title_threshold

    # --------------------------
    # Compare authors with set intersection
    # --------------------------
    def _compare_authors(self, authors_ref: List[str], authors_meta: List[str]) -> bool:
        if not authors_ref or not authors_meta:
            return False
        # Consider match if >=70% of authors in reference appear in metadata
        matches = len(set(a.lower() for a in authors_ref) & set(a.lower() for a in authors_meta))
        ratio = matches / max(len(authors_ref), len(authors_meta))
        return ratio >= 0.97#0.7

    # --------------------------
    # Compare title with fuzzy ratio
    # --------------------------
    def _compare_title(self, title_ref: Optional[str], title_meta: Optional[str]) -> bool:
        if not title_ref or not title_meta:
            return False
        ratio = SequenceMatcher(None, title_ref.lower(), title_meta.lower()).ratio()
        return ratio >=0.97 #self.title_threshold

    # --------------------------
    # Verify reference
    # --------------------------
    def verify_reference(self, ref: Dict) -> Dict:
        parsed = ref["parsed"]
        doi = parsed.get("doi")
        authors = parsed.get("authors")
        year = parsed.get("year")
        title = parsed.get("title")

        if doi:
            valid, crossref_meta = self.verifier.verify_doi(doi)
            
            if not valid:
                return {
                    "status": "invalid_doi",
                    "reason": "DOI not found in Crossref",
                    "crossref_metadata": None
                }
            
            # controlli
            author_ok = self._compare_authors(authors, crossref_meta.get("authors", []))
            year_ok = (year == crossref_meta.get("year")) if year else False
            title_ok = self._compare_title(title, crossref_meta.get("title"))

            # Caso DOI valido e metadati sufficientemente corretti
            if author_ok and year_ok and title_ok:
                return {
                    "status": "verified",
                    "author_match": True,
                    "year_match": True,
                    "title_match": True,
                    "crossref_metadata": crossref_meta
                }
            else:
                # DOI valido ma qualche discrepanza nei metadati
                return {
                    "status": "metadata_mismatch",
                    "author_match": author_ok,
                    "year_match": year_ok,
                    "title_match": title_ok,
                    "crossref_metadata": crossref_meta
                }

        # Caso senza DOI
        if authors and year:
            return {
                "status": "insufficient_metadata",
                "reason": "No DOI. Author-year citations cannot be verified reliably.",
                "crossref_matches": [],
                "title_match": None
            }

        return {
            "status": "insufficient_metadata",
            "reason": "Missing DOI and insufficient structured fields",
            "crossref_matches": []
        }

    # --------------------------
    # Main run
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

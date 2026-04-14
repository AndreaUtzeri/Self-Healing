import re
from typing import Dict, Any


class CitationAct:
    """
    New version of ACT: corrects, normalizes, or removes citations
    based on the PLAN results.
    """

    def __init__(self):
        pass

    # --------------------------------------------------------------
    # 1. Reconstruct correct citation based on Crossref
    # --------------------------------------------------------------
    def _format_correct_reference(self, metadata: Dict[str, Any], doi: str) -> str:
        authors = metadata.get("authors", [])
        year = metadata.get("year", "n.d.")
        title = metadata.get("title", "Unknown title")
        venue = metadata.get("venue", "Unknown venue")

        # Authors in simplified APA style: first author et al.
        if len(authors) == 0:
            author_str = ""
        elif len(authors) == 1:
            author_str = authors[0]
        else:
            author_str = f"{authors[0]} et al."

        return f"{author_str} ({year}). {title}. {venue}. https://doi.org/{doi}"

    # --------------------------------------------------------------
    # 2. Apply transformations to the text
    # --------------------------------------------------------------
    def apply(self, text: str, plan_output: Dict[str, Dict]) -> str:
        """
        text: original text
        plan_output: output of the PLAN with verification status
        """
        adapted = text

        for ref_id, ref_data in plan_output.items():
            detected = ref_data["detected_form"]
            parsed = ref_data["parsed"]
            verification = ref_data["verification"]
            status = verification["status"]

            # Escape the detected string as it appears in the text
            pattern = re.escape(detected)

            # -----------------------------------------------
            # Case A: DOI verified → correct the citation
            # -----------------------------------------------
            if status == "verified":
                doi = parsed["doi"]
                crossref_meta = verification["crossref_metadata"]
                corrected = self._format_correct_reference(crossref_meta, doi)
                adapted = re.sub(pattern, corrected, adapted)
                continue

            # -----------------------------------------------
            # Case B: DOI NOT valid → remove completely
            # -----------------------------------------------
            if status == "invalid_doi":
                adapted = re.sub(pattern, "[[OMIT_INVALID_DOI]]", adapted)
                continue

            # -----------------------------------------------
            # Case C: citation not verifiable
            # -----------------------------------------------
            if status == "insufficient_metadata":
                replacement = f"{detected} [UNVERIFIABLE]"
                adapted = re.sub(pattern, replacement, adapted)
                continue

        return adapted
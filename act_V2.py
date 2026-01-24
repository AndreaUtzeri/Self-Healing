import re
from typing import Dict, Any


class CitationAct:
    """
    Nuova versione dell'ACT: corregge, normalizza o rimuove citazioni
    in base ai risultati del PLAN.
    """

    def __init__(self):
        pass

    # --------------------------------------------------------------
    # 1. Ricostruzione citazione corretta basata su Crossref
    # --------------------------------------------------------------
    def _format_correct_reference(self, metadata: Dict[str, Any], doi: str) -> str:
        authors = metadata.get("authors", [])
        year = metadata.get("year", "n.d.")
        title = metadata.get("title", "Unknown title")
        venue = metadata.get("venue", "Unknown venue")

        # Autori stile APA ridotto: Primo autore et al.
        if len(authors) == 0:
            author_str = ""
        elif len(authors) == 1:
            author_str = authors[0]
        else:
            author_str = f"{authors[0]} et al."

        return f"{author_str} ({year}). {title}. {venue}. https://doi.org/{doi}"

    # --------------------------------------------------------------
    # 2. Applica trasformazioni al testo
    # --------------------------------------------------------------
    def apply(self, text: str, plan_output: Dict[str, Dict]) -> str:
        """
        text: testo originale
        plan_output: output del PLAN con status di verifica
        """
        adapted = text

        for ref_id, ref_data in plan_output.items():
            detected = ref_data["detected_form"]
            parsed = ref_data["parsed"]
            verification = ref_data["verification"]
            status = verification["status"]

            # Escaping della stringa catturata nel testo
            pattern = re.escape(detected)

            # -----------------------------------------------
            # Caso A: DOI verificato → correggi
            # -----------------------------------------------
            if status == "verified":
                doi = parsed["doi"]
                crossref_meta = verification["crossref_metadata"]
                corrected = self._format_correct_reference(crossref_meta, doi)
                adapted = re.sub(pattern, corrected, adapted)
                continue

            # -----------------------------------------------
            # Caso B: DOI NON valido → elimina completamente
            # -----------------------------------------------
            if status == "invalid_doi":
                adapted = re.sub(pattern, "[[OMIT_INVALID_DOI]]", adapted)
                continue

            # -----------------------------------------------
            # Caso C: cita­zione non verificabile
            # -----------------------------------------------
            if status == "insufficient_metadata":
                replacement = f"{detected} [UNVERIFIABLE]"
                adapted = re.sub(pattern, replacement, adapted)
                continue

        return adapted

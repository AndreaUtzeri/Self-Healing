import re
from typing import Dict, Tuple

class CitationAct:
    def __init__(self):
        pass

    def adapt_text(self, text: str, verification_results: Dict[str, Tuple[bool, dict]]) -> str:
        """
        Adatta il testo sostituendo DOI non validi con [[OMIT]] e arricchendo DOI validi con metadati.
        Gestisce DOI con prefisso (https://doi.org/) o DOI "nudi".
        """
        adapted_text = text

        for doi, (is_valid, metadata) in verification_results.items():
            # Escapiamo il DOI per usarlo in regex
            doi_pattern = re.escape(doi)
            # Pattern per catturare tutte le varianti di DOI
            full_pattern = rf"(https?://(dx\.)?doi\.org/)?{doi_pattern}"

            if not is_valid:
                replacement = "[[OMIT]]"
            else:
                title = metadata.get('title', 'Titolo sconosciuto') if metadata else 'Titolo sconosciuto'
                year = metadata.get('year', 'Anno sconosciuto') if metadata else 'Anno sconosciuto'
                replacement = f"{doi} (\"{title}\", {year})"

            # Sostituisce tutte le occorrenze con o senza prefisso
            adapted_text = re.sub(full_pattern, replacement, adapted_text)

        return adapted_text

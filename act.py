from typing import Dict, Tuple

class CitationAct:
    def __init__(self):
        pass

    def adapt_text(self, text: str, verification_results: Dict[str, Tuple[bool, dict]]) -> str:
        """
        Applica le azioni correttive in base ai risultati del verifier.

        Args:
            text: testo originale (output del modello)
            verification_results: dizionario {doi: (is_valid, metadata)}

        Returns:
            testo corretto/adattato
        """

        adapted_text = text

        for doi, (is_valid, metadata) in verification_results.items():
            if not is_valid:

                replacement = "[[OMIT]]"#f"__"#f"[DOI rimosso: {doi}]"
                #adapted_text = adapted_text.replace(doi, replacement)
                #Sostituisco varianti diverse del doi
                adapted_text = adapted_text.replace(f"https://doi.org/{doi}", replacement)
                adapted_text = adapted_text.replace(f"http://doi.org/{doi}", replacement)
                adapted_text = adapted_text.replace(f"https://dx.doi.org/{doi}", replacement)
                adapted_text = adapted_text.replace(f"http://dx.doi.org/{doi}", replacement)

            else:
                title = metadata.get('title', 'Titolo sconosciuto') if metadata else None
                year = metadata.get('year', 'Anno sconosciuto') if metadata else None
                enriched_info = f"{doi} (\"{title}\", {year})"
                adapted_text = adapted_text.replace(f"https://doi.org/{doi}", enriched_info)
                adapted_text = adapted_text.replace(f"http://doi.org/{doi}", enriched_info)
                adapted_text = adapted_text.replace(f"https://dx.doi.org/{doi}", enriched_info)
                adapted_text = adapted_text.replace(f"http://dx.doi.org/{doi}", enriched_info)


        return adapted_text
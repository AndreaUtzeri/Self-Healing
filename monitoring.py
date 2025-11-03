import re
from typing import List, Dict

class CitationMonitor:
    def __init__(self):
        self.doi_pattern = r'https?://(?:dx\.)?doi\.org/([^\s\'")]+)' #r'\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b' regex più restrittiva
        self.compiled_pattern = re.compile(self.doi_pattern)

    def extract_dois(self, text: str) -> List[str]:
        # Trova DOI nel formato URL (es. https://doi.org/10.1038/nphys1170)
        dois = self.compiled_pattern.findall(text)

        
        cleaned_dois = [doi.strip().strip(",.;()[]{}") for doi in dois]

        
        unique_dois = list(dict.fromkeys(cleaned_dois))

        return unique_dois

    def locate_dois(self, text:str ) -> List[Dict]:

        location= []

        for match in self.compiled_pattern.finditer(text): #finditer e non findall perche il primo mi reestituisce un oggetto match che contiene info sulla posizione del match

            doi = match.group(1) #group estrae il contenuto del match

            full_match = match.group(0)

            start = match.start()  #la posizione di partenza del match

            end = match.end()   #la posizione di fine del match

            context_start = max(0, start - 50)
            context_end = min(len(text), end + 50)
            context = text[context_start:context_end]

            location.append({
                'doi': doi,
                'full_match': full_match,
                'start': start,
                'end': end,
                'context': context
            })
        return location

    """
    Locatee_lois lo uso per sapere la posizione del doi nel testo per poi andare a fare
    eventuali correzioni, mi serve restituire una lista di dizionari in quanto per ogni doi
    il valore del doi, start, end.
    Con context_start prendo il contesto del doi 50 caratteri prima e dopo il doi
    infatti prendo il massimo tra 0 e start-50 per evitare di andare in negativo
    stesso discorso per il context end. Lo calcolo in quanto in futuro potrebbe essere utile
    Ad esempio per un eventuale implementazione interna al rtransformer che tenga conto del contesto per capire i propri errori


    """
import requests
from typing import Optional, Tuple, Dict
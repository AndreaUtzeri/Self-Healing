import requests
from typing import Optional, Tuple, Dict


class CitationVerifier:

    def __init__(self):

        self.base_url = "https://api.crossref.org/works/"
        self.api_calls = 0

    def verify_doi(self, doi: str, timeout: int = 5 ) -> Tuple[bool, Optional[Dict]]:  #optional in quanto può non essere none
        # voglio ritornare una tupla che mi dice se il doi è valido, e i suoi metadati
        self.api_calls += 1
        url = self.base_url + doi
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                data = response.json() #viene convertito in dizionario
                message = data['message']
                metadata = {
                    'title': message.get('title', ['Sconosciuto'])[0],
                    'authors': self._extract_authors(message),
                    'year': self._extract_year(message),
                    'publisher': message.get('publisher', 'Sconosciuto')
                }
                return True, metadata
            elif response.status_code == 404:
                return False, None
        except requests.Timeout:
            print(f"Timeout verificando DOI {doi}")
            return False, None

        except Exception as e:
            print(f"Errore verificando DOI {doi}: {e}")
            return False, None

    def _extract_authors(self, message: Dict) -> list:
        """Estrae cognomi autori (max 3)"""
        authors = message.get('author', [])
        author_names = []
        for author in authors[:3]:
            family_name = author.get('family', '')
            if family_name:
                author_names.append(family_name)
        return author_names

    def _extract_year(self, message: Dict) -> Optional[int]:
        """Estrae anno di pubblicazione"""
        date_fields = ['published-print', 'published-online', 'issued']
        for field in date_fields:
            date_info = message.get(field, {})
            if date_info:
                date_parts = date_info.get('date-parts', [[]])
                if date_parts and date_parts[0]:
                    year = date_parts[0][0]
                    if year:
                        return year
        return None

    def get_stats(self) -> Dict:
        """Statistiche sull'uso"""
        return {
            'api_calls': self.api_calls
        }
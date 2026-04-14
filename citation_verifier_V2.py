import requests
from typing import Optional, Tuple, Dict, List


class CitationVerifier:

    def __init__(self):
        self.base_url = "https://api.crossref.org/works/"
        self.search_url = "https://api.crossref.org/works"
        self.api_calls = 0


    # =======================================================================
    # VERIFICA DOIs
    # =======================================================================
    def verify_doi(self, doi: str, timeout: int = 5) -> Tuple[bool, Optional[Dict]]:
        """
        Verifica un DOI tramite Crossref. Restituisce (valid, metadata).
        """
        self.api_calls += 1
        url = self.base_url + doi

        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                message = data["message"]

                metadata = {
                    "title": message.get("title", ["Unknown"])[0],
                    "authors": self._extract_author_list(message),
                    "year": self._extract_year(message),
                    "venue": message.get("container-title", ["Unknown"])[0],
                    "publisher": message.get("publisher", "Unknown")
                }
                return True, metadata

            return False, None

        except Exception as e:
            print(f"[Verifier] Error verifying DOI {doi}: {e}")
            return False, None


    # =======================================================================
    # SEARCH: AUTHOR + YEAR
    # =======================================================================
    def search_by_author_year(self, author: str, year: int, timeout: int = 5) -> List[Dict]:
        
        params = {
            "query.author": author,
            "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
            "rows": 5
        }

        try:
            response = requests.get(self.search_url, params=params, timeout=timeout)
            data = response.json()

            items = data.get("message", {}).get("items", [])
            return [self._extract_metadata_from_item(x) for x in items]

        except Exception as e:
            print(f"[Verifier] Author-year search error: {e}")
            return []


    # =======================================================================
    # SEARCH: TITLE (bibliographic search)
    # =======================================================================
    def search_by_title(self, title: str, timeout: int = 5) -> List[Dict]:
        """
        Cerca il titolo in Crossref. Potrebbe contenere match inesatti.
        """
        params = {
            "query.bibliographic": title,
            "rows": 5
        }

        try:
            response = requests.get(self.search_url, params=params, timeout=timeout)
            data = response.json()
            items = data.get("message", {}).get("items", [])
            return [self._extract_metadata_from_item(x) for x in items]

        except Exception as e:
            print(f"[Verifier] Title search error: {e}")
            return []


    # =======================================================================
    # HELPERS
    # =======================================================================
    def _extract_year(self, message: Dict) -> Optional[int]:
        fields = ["published-print", "published-online", "issued"]
        for f in fields:
            parts = message.get(f, {}).get("date-parts", [[]])
            if parts and len(parts[0]) > 0:
                return parts[0][0]
        return None

    def _extract_author_list(self, message: Dict) -> List[str]:
        authors = message.get("author", [])
        result = []
        for a in authors:
            if "family" in a:
                result.append(a["family"])
        return result[:5]

    def _extract_metadata_from_item(self, item: Dict) -> Dict:
      
        return {
            "doi": item.get("DOI"),
            "title": item.get("title", ["Unknown"])[0],
            "authors": self._extract_author_list(item),
            "year": self._extract_year(item),
            "venue": item.get("container-title", ["Unknown"])[0],
            "publisher": item.get("publisher", "Unknown")
        }


    def get_stats(self) -> Dict:
        return {
            "api_calls": self.api_calls
        }

from api_openai import OpenAIClient
import re

class CitationRefiner:
    def __init__(self, client):
        self.client = client

    def refine_sentence(self, sentence: str) -> str:
        """Corregge la sintassi di una singola frase con placeholder [[OMIT]]."""
        content = (
            "Sei un assistente che corregge la grammatica e la sintassi di testi accademici. "
            
        )

        prompt = (
            f"Riscrivi questa frase in modo grammaticalmente corretto e fluido, "
            f"elimando i placeholder [[OMIT]] e riformulando la frase dopo la loro eliminazione:\n\n{sentence}"
        )

        refined = self.client.generate_text(content, prompt)
        return refined.strip()

    def refine_text(self, text: str) -> str:
        """
        Versione ottimizzata:
        - Estrae tutte le frasi contenenti [[OMIT]].
        - Rimuove duplicati.
        - Le invia tutte insieme in un'unica chiamata al modello.
        - Ricostruisce il testo sostituendo solo le frasi corrette.
        """
        print("\n=== DEBUG: Refining per contesto (ottimizzato) ===")

        # Suddivisione del testo in frasi
        sentences = re.split(r'(?<=[.!?])\s+', text)
        print(f"Frasi trovate: {len(sentences)}")

        # Filtra solo le frasi che contengono [[OMIT]]
        sentences_to_refine = [s for s in sentences if "[[OMIT]]" in s]
        sentences_to_refine = list(set(sentences_to_refine))  # rimuovi duplicati

        if not sentences_to_refine:
            print("[DEBUG] Nessuna frase da correggere.")
            return text

        print(f"Frasi da inviare al modello: {len(sentences_to_refine)}")

        # Prepara prompt unificato
        content = (
            "Sei un assistente che corregge la grammatica e la sintassi di testi accademici. "
            "Rimuovi i placeholder [[OMIT]] e riformula le frasi in modo fluido e coerente. "
            "Restituisci le frasi corrette nello stesso ordine, separate da '---'."
        )

        joined_sentences = "\n---\n".join(sentences_to_refine)
        prompt = f"Ecco le frasi da correggere:\n\n{joined_sentences}"

        # Una sola chiamata al modello
        refined_block = self.client.generate_text(content, prompt)["text"]
        refined_sentences = [s.strip() for s in refined_block.split('---') if s.strip()]

        # Verifica che il numero di frasi corrisponda
        if len(refined_sentences) != len(sentences_to_refine):
            print("[AVVISO] Il numero di frasi corrette non corrisponde a quello originale. "
                  "Potrebbero esserci discrepanze minori nell'allineamento.")

        # Ricostruzione del testo finale
        final_text = text
        for original, refined in zip(sentences_to_refine, refined_sentences):
            final_text = final_text.replace(original, refined)

        result = self.client.generate_text(content, prompt)
        print("[DEBUG] Review completata (testo intero)")
        return result["text"], result  # restituisci testo + metriche
    
    def refine_full_text(self, text: str) -> str:
        
        content = (
            "Sei un assistente che corregge la grammatica e la sintassi di testi accademici. "
            "Il testo può contenere placeholder [[OMIT]] che rappresentano citazioni rimosse."
        )

        prompt = (
            f"Riscrivi il testo seguente rendendolo grammaticalmente corretto e coerente, "
            f"senza modificare il contenuto, ma rimuovendo i placeholder [[OMIT]]:\n\n{text}"
        )

        result = self.client.generate_text(content, prompt)
        print("[DEBUG] Review completata (testo intero)")
        return result["text"], result 
    
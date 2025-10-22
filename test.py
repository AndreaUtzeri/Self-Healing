from MPA_module import SelfHealingLayer
from api_openai import OpenAIClient


generator = OpenAIClient()  
topic = "Effetti della computazione quantistica sulla sicurezza dei dati"
content = "Sei un assistente che genera testi accademici con riferimenti DOI integrati nella struttura delle frasi."
prompt = (
    "Scrivi un testo accademico di circa massimo 1000 parole sulla fisica quantistica. "
    "Il testo deve contenere riferimenti DOI integrati DENTRO la struttura delle frasi, "
    "non tra parentesi e non come note bibliografiche.\n\n"

    "REQUISITI PER I DOI:\n"
    "- Inserisci almeno 3 DOI inventati nel formato https://doi.org/10.1000/xxxxxxx.\n"
    "- Inserisci almeno 3 DOI REALI presi da articoli scientifici autentici su fisica quantistica, "
    "preferibilmente pubblicati su riviste come Nature, Science, Physical Review Letters o simili.\n"
    "- I DOI reali devono essere effettivamente esistenti (non inventarli) e coerenti con il contenuto.\n"
    "- Alterna DOI veri e inventati in modo naturale nel testo.\n\n"

    "ESEMPI CORRETTI (DOI che causano errori se rimossi):\n"
    "- 'Secondo https://doi.org/10.1000/xyz123 la sovrapposizione quantistica...'\n"
    "- 'Il https://doi.org/10.1038/nphys1170 dimostra che...'\n"
    "- 'Come riportato in https://doi.org/10.1103/PhysRevLett.116.061102 del 2016, gli effetti...'\n"
    "- 'Lo studio https://doi.org/10.1000/ghi012 ha rivelato...'\n\n"

    "ESEMPI SBAGLIATI (da NON usare):\n"
    "- 'La fisica quantistica (https://doi.org/...) è importante' \n"
    "- 'Secondo lo studio (Smith, 2021; https://doi.org/...) la teoria' \n\n"

    "Assicurati che i DOI (veri e inventati) siano distribuiti in tutto il testo e integrati nella sintassi delle frasi in modo naturale."
)

text = generator.generate_text(content, prompt)

print("\n=== TESTO GENERATO ===\n")
print(text)

    
citation_module = SelfHealingLayer()
result = citation_module.process_text(text)



print("\n=== TESTO ADATTATO ===")
print(result["adapted_text"])

print("\n=== TESTO RAFFINATO (solo frasi con [[OMIT]]) ===")
print(result["refined_text_sentence_based"])

print("\n=== TESTO RAFFINATO (intero) ===")
print(result["refined_text_full"])

print("\n=== STATISTICHE ===")
print(result["stats"])

import pandas as pd
from api_openai import OpenAIClient
from MPA_module import SelfHealingLayer

class ReviewExperiment:
    def __init__(self, topics: list):
        self.topics = topics
        self.client = OpenAIClient()
        self.layer = SelfHealingLayer()
        self.results = []

    def run(self):
        for topic in self.topics:
            print(f"\n TEST SU: {topic}")
            prompt = (
            "Scrivi un testo accademico di circa 800 parole sul '{topic}' "
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

            gen_result = self.client.generate_text(
                "Sei un assistente che genera testi accademici con DOI.",
                prompt,
            )
            text = gen_result["text"]

            result = self.layer.process_text(text)

            self.results.append({
                "topic": topic,
                "prompt_tokens_full": result["metrics_full"].get("prompt_tokens", 0),
                "prompt_tokens_sent": result["metrics_sentence"].get("prompt_tokens", 0),
                "total_tokens_full": result["metrics_full"].get("total_tokens", 0),
                "total_tokens_sent": result["metrics_sentence"].get("total_tokens", 0),
                "cost_full": result["metrics_full"].get("cost", 0),
                "cost_sent": result["metrics_sentence"].get("cost", 0),
                "latency_full": result["metrics_full"].get("latency", 0),
                "latency_sent": result["metrics_sentence"].get("latency", 0),
                "saving_pct_tokens": (
                    1 - result["metrics_sentence"].get("total_tokens", 1)
                    / max(result["metrics_full"].get("total_tokens", 1), 1)
                ) * 100,
                "saving_pct_cost": (
                    1 - result["metrics_sentence"].get("cost", 1)
                    / max(result["metrics_full"].get("cost", 1), 1)
                ) * 100,
                "total_time_pipeline": result["total_time"],
            })

        # Salva CSV finale
        df = pd.DataFrame(self.results)
        df.to_csv("review_experiment_results.csv", index=False)
        print("\n Risultati salvati in 'review_experiment_results.csv'")

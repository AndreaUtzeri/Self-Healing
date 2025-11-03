import pandas as pd
from api_openai import OpenAIClient
from MPA_module import SelfHealingLayer

class AccuracyExperiment:
    def __init__(self, topics: list):
        self.topics = topics
        self.client = OpenAIClient()
        self.layer = SelfHealingLayer()
        self.results = []

    def run(self):
        for topic in self.topics:
            print(f"\n=== TEST SU: {topic} ===")

            # Prompt SENZA istruzioni su DOI inventati
            prompt = (
                "Scrivi un testo accademico di circa 800 parole sul '{topic}' "
                "Il testo deve contenere riferimenti DOI integrati DENTRO la struttura delle frasi, "
                "non tra parentesi e non come note bibliografiche.\n\n"

                "REQUISITI PER I DOI:\n"
                "preferibilmente pubblicati su riviste come Nature, Science, Physical Review Letters o simili.\n"
                "ESEMPI CORRETTI (DOI che causano errori se rimossi):\n"
                "- 'Secondo https://doi.org/10.1000/xyz123 la sovrapposizione quantistica...'\n"
                "- 'Il https://doi.org/10.1038/nphys1170 dimostra che...'\n"
                "- 'Come riportato in https://doi.org/10.1103/PhysRevLett.116.061102 del 2016, gli effetti...'\n"
                "- 'Lo studio https://doi.org/10.1000/ghi012 ha rivelato...'\n\n"

                "ESEMPI SBAGLIATI (da NON usare):\n"
                "- 'La fisica quantistica (https://doi.org/...) è importante' \n"
                "- 'Secondo lo studio (Smith, 2021; https://doi.org/...) la teoria' \n\n"

            )  

            gen_result = self.client.generate_text(
                "Sei un assistente che scrive testi accademici accurati con DOI reali.",
                prompt,
            )
            text = gen_result["text"]

            # Passa il testo alla pipeline
            result = self.layer.process_text(text)

            # Estrai DOI rilevati
            detected_dois = self.layer.monitor.extract_dois(text)

            # Estrai metriche di accuratezza
            total_dois = result["num_dois"]
            invalid_dois = result["num_invalid_dois"]
            valid_dois = total_dois - invalid_dois

            # Calcola metriche di accuratezza
            detection_rate = invalid_dois / total_dois * 100 if total_dois > 0 else 0

            # Numero di DOI effettivamente corretti
            corrected_dois = sum("[[OMIT]]" in result["adapted_text"] for _ in range(invalid_dois))
            correction_rate = corrected_dois / invalid_dois * 100 if invalid_dois > 0 else 0

            self.results.append({
                "topic": topic,
                "num_dois": total_dois,
                "num_invalid_dois": invalid_dois,
                "num_valid_dois": valid_dois,
                "detection_rate_%": detection_rate,
                "correction_rate_%": correction_rate,
                "doi_list": ", ".join(detected_dois),  # <- qui aggiungiamo i DOI rilevati
                "total_time_pipeline": result["total_time"],
            })

        # Salva CSV finale
        df = pd.DataFrame(self.results)
        df.to_csv("accuracy_experiment_results.csv", index=False)
        print("\n✅ Risultati salvati in 'accuracy_experiment_results.csv'")

import pandas as pd
import statistics
from tqdm import tqdm
from MPA_module import SelfHealingLayer
from api_openai import OpenAIClient

class AccuracyExperiment:
    """
    Esegue test di accuratezza sui DOI generati da modelli linguistici
    e mostra l'evoluzione del testo (originale → adattato → raffinato).
    """
    def __init__(self, topics: list):
        self.topics = topics
        self.client = OpenAIClient()
        self.layer = SelfHealingLayer()
        self.results = []

    def run(self, n_samples_per_topic: int = 1):
        """
        Esegue l'esperimento su ciascun topic, generando più campioni per topic.
        """
        for topic in self.topics:
            print(f"\n=== TEST SU: {topic} ===")

            for i in range(n_samples_per_topic):
                print(f"\n🧪 ESECUZIONE {i+1}/{n_samples_per_topic} per topic: {topic}")

                # === 1️⃣ GENERAZIONE TESTO ORIGINALE ===
                prompt = (
                    f"Scrivi un testo accademico di circa 800 parole sul '{topic}'. "
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
                    "- 'La fisica quantistica (https://doi.org/...) è importante'\n"
                    "- 'Secondo lo studio (Smith, 2021; https://doi.org/...) la teoria'\n"
                )

                gen_result = self.client.generate_text(
                    "Sei un assistente che scrive testi accademici accurati con DOI reali.",
                    prompt,
                )
                text_original = gen_result["text"]

                # === 2️⃣ PIPELINE SELF-HEALING ===
                result = self.layer.process_text(text_original)

                text_adapted = result["adapted_text"]
                text_refined = (
                    result["refined_text_full"]
                    or result["refined_text_sentence_based"]
                )

                # === 3️⃣ ESTRAZIONE METRICHE ===
                detected_dois = self.layer.monitor.extract_dois(text_original)
                total_dois = result["num_dois"]
                invalid_dois = result["num_invalid_dois"]
                valid_dois = total_dois - invalid_dois
                detection_rate = invalid_dois / total_dois * 100 if total_dois > 0 else 0
                corrected_dois = sum("[[OMIT]]" in result["adapted_text"] for _ in range(invalid_dois))
                correction_rate = corrected_dois / invalid_dois * 100 if invalid_dois > 0 else 0

                # === 4️⃣ STAMPA EVOLUZIONE TESTO ===
                print("\n📘 EVOLUZIONE TESTO:")
                print("\n--- [ORIGINALE] ---\n", text_original[:800], "...\n")
                print("\n--- [ADATTATO - CON PLACEHOLDER] ---\n", text_adapted[:800], "...\n")
                print("\n--- [RAFFINATO FINALE] ---\n", text_refined[:800], "...\n")

                # === 5️⃣ SALVATAGGIO RISULTATI ===
                self.results.append({
                    "topic": topic,
                    "sample_id": i + 1,
                    "num_dois": total_dois,
                    "num_invalid_dois": invalid_dois,
                    "num_valid_dois": valid_dois,
                    "detection_rate_%": detection_rate,
                    "correction_rate_%": correction_rate,
                    "doi_list": ", ".join(detected_dois),
                    "total_time_pipeline": result["total_time"],
                    "text_original": text_original,
                    "text_adapted": text_adapted,
                    "text_refined_final": text_refined,
                })

        # === 6️⃣ SALVATAGGIO CSV ===
        df = pd.DataFrame(self.results)
        df.to_csv("accuracy_experiment_results.csv", index=False)
        print("\n✅ Risultati salvati in 'accuracy_experiment_results.csv' con evoluzione del testo")

    def summarize(self):
        """Analisi finale aggregata dopo tutti i test."""
        if not self.results:
            print("⚠️ Nessun risultato disponibile.")
            return

        df = pd.DataFrame(self.results)
        df.to_csv("accuracy_experiment_results.csv", index=False)

        print("\n📊 RISULTATI GLOBALI")
        total_dois = df["num_dois"].sum()
        total_invalid = df["num_invalid_dois"].sum()
        total_valid = df["num_valid_dois"].sum()
        mean_detection = df["detection_rate_%"].mean()
        mean_correction = df["correction_rate_%"].mean()
        mean_time = statistics.mean(df["total_time_pipeline"])

        print(f"🔹 DOI totali analizzati: {total_dois}")
        print(f"🔹 DOI validi: {total_valid}  |  Invalidi: {total_invalid}")
        print(f"🔹 Tasso medio DOI allucinati: {mean_detection:.2f}%")
        print(f"🔹 Tasso medio correzione: {mean_correction:.2f}%")
        print(f"🔹 Tempo medio elaborazione: {mean_time:.2f} sec/testo")
        print("\n✅ Dati salvati in 'accuracy_experiment_results.csv'")


# ==============================
# 🚀 MAIN ESEGUIBILE
# ==============================
if __name__ == "__main__":
    topics = [
        "Quantum computing and decoherence",
        "Deep learning in medical imaging",
        "Climate change modeling and prediction",
        "Nanomaterials for energy storage",
        "Language models in scientific writing",
    ]

    n_samples_per_topic = 2  # puoi aumentare per più test per topic

    exp = AccuracyExperiment(topics)

    print("\n🚀 Avvio esperimento di accuratezza...")
    for _ in tqdm(range(1), desc="Ciclo principale"):  # 1 ciclo esterno
        exp.run(n_samples_per_topic=n_samples_per_topic)

    exp.summarize()

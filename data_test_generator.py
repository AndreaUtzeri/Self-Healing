import random

GROUND_TRUTH = [
    {
      "id": "GT01",
      "authors": ["Krizhevsky", "Sutskever", "Hinton"],
      "year": 2017,
      "doi": "10.1145/3065386",
      "title": "ImageNet classification with deep convolutional neural networks",
      "venue": "Communications of the ACM"
    },
    {
      "id": "GT02",
      "authors": ["Hochreiter", "Schmidhuber"],
      "year": 1997,
      "doi": "10.1162/neco.1997.9.8.1735",
      "title": "Long Short-Term Memory",
      "venue": "Neural Computation"
    },
    {
      "id": "GT03",
      "authors": ["Pan", "Yang"],
      "year": 2010,
      "doi": "10.1109/TKDE.2010.191",
      "title": "A Survey on Transfer Learning",
      "venue": "IEEE Transactions on Knowledge and Data Engineering"
    },
    {
      "id": "GT04",
      "authors": ["Almanjahie", "Kaid", "Laksaci", "Rachdi"],
      "year": 2021,
      "doi": "10.7717/peerj.11719",
      "title": "Predicting temperature curve based on fast kNN local linear estimation of the conditional distribution function",
      "venue": "PeerJ"
    },
    
  {
  "id": "GT06",
  "authors": ["Bartlett"],
  "year": 2014,
  "doi": "10.5860/llm.v29i1.7116",
  "title": "New and Noteworthy: Coming to Terms with Librarian Stereotypes and Self-Image",
  "venue": "Library Leadership & Management"
  }
]

# ---- FUNZIONE PER GENERARE RIFERIMENTI ----
def make_reference(ref, corruption_type=None):
    """Genera una citazione bibliografica a partire da un record ground truth."""
    authors_str = ", ".join(ref["authors"])
    year = ref["year"]
    title = ref["title"]
    venue = ref["venue"]
    doi = ref["doi"]

    # Diversi tipi di corruzione controllata
    if corruption_type == "title":
        title = title.replace("the", "a", 1) + " (misstated title)"
    elif corruption_type == "authors":
        authors_str = authors_str + ", Smith"  # aggiunge autore errato
    elif corruption_type == "year":
        year = year + random.choice([-2, -1, 1, 2])
    elif corruption_type == "metadata_combo":
        title = "Modified version of " + title
        authors_str = authors_str.replace(ref["authors"][0], "WrongAuthor")
    elif corruption_type == "invalid_doi":
        doi = "10.fake/" + str(random.randint(1000, 9999))
    elif corruption_type == "partial":
        return f"{ref['authors'][0]} ({ref['year']}) mentioned this topic."

    return f"{authors_str} ({year}). {title}. {venue}. DOI: {doi}."

# ---- GENERAZIONE TEST SET ----
CORRUPTION_TYPES = [
    None,  # riferimento corretto
    "title",
    "authors",
    "year",
    "metadata_combo",
    "invalid_doi",
    "partial"
]

TEST_REFERENCES = []
counts = {"true": 0, "corrupt": 0, "partial": 0}

for i in range(300):
    ref = random.choice(GROUND_TRUTH)
    corruption_type = random.choices(
        CORRUPTION_TYPES,
        weights=[0.3, 0.1, 0.1, 0.1, 0.1, 0.15, 0.15],  # 30% veri, 70% corrotti/parziali
        k=1
    )[0]

    citation_text = make_reference(ref, corruption_type)

    # Etichetta ground truth
    if corruption_type is None:
        label = "true"
        counts["true"] += 1
    elif corruption_type == "partial":
        label = "partial"
        counts["partial"] += 1
    else:
        label = "corrupt"
        counts["corrupt"] += 1

    TEST_REFERENCES.append({
        "text": citation_text,
        "label": label
    })


for r in TEST_REFERENCES[:12]:
    print(r["text"])

# ---- STATISTICHE ----
print("\n=== GENERATION SUMMARY ===")
print(f"Totale riferimenti generati: {len(TEST_REFERENCES)}")
print(f"   Correttamente intatti: {counts['true']}")
print(f"   Corrotti: {counts['corrupt']}")
print(f"   Parziali (non verificabili): {counts['partial']}")
print(f"   Percentuali → Intatti: {counts['true']/len(TEST_REFERENCES)*100:.1f}%, "
      f"Corrotti: {counts['corrupt']/len(TEST_REFERENCES)*100:.1f}%, "
      f"Parziali: {counts['partial']/len(TEST_REFERENCES)*100:.1f}%")

import random

GROUND_TRUTH = [
    # ---- Computer Vision / Deep Learning ----
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
        "authors": ["He", "Zhang", "Ren", "Sun"],
        "year": 2016,
        "doi": "10.1109/CVPR.2016.90",
        "title": "Deep residual learning for image recognition",
        "venue": "Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition"
    },
    # ---- NLP / Sequence Models ----
    {
        "id": "GT03",
        "authors": ["Hochreiter", "Schmidhuber"],
        "year": 1997,
        "doi": "10.1162/neco.1997.9.8.1735",
        "title": "Long Short-Term Memory",
        "venue": "Neural Computation"
    },
    {
        "id": "GT04",
        "authors": ["Vaswani", "Shazeer", "Parmar", "Uszkoreit", "Jones", "Gomez", "Kaiser", "Polosukhin"],
        "year": 2017,
        "doi": "10.48550/arXiv.1706.03762",
        "title": "Attention is all you need",
        "venue": "Advances in Neural Information Processing Systems"
    },
    # ---- Transfer Learning ----
    {
        "id": "GT05",
        "authors": ["Pan", "Yang"],
        "year": 2010,
        "doi": "10.1109/TKDE.2010.191",
        "title": "A Survey on Transfer Learning",
        "venue": "IEEE Transactions on Knowledge and Data Engineering"
    },
    # ---- Statistics / Machine Learning ----
    {
        "id": "GT06",
        "authors": ["Almanjahie", "Kaid", "Laksaci", "Rachdi"],
        "year": 2021,
        "doi": "10.7717/peerj.11719",
        "title": "Predicting temperature curve based on fast kNN local linear estimation of the conditional distribution function",
        "venue": "PeerJ"
    },
    {
        "id": "GT07",
        "authors": ["Ioffe", "Szegedy"],
        "year": 2015,
        "doi": "10.48550/arXiv.1502.03167",
        "title": "Batch normalization: accelerating deep network training by reducing internal covariate shift",
        "venue": "International Conference on Machine Learning"
    },
    # ---- Reinforcement Learning ----
    {
        "id": "GT08",
        "authors": ["Mnih", "Kavukcuoglu", "Silver", "Graves", "Antonoglou", "Wierstra", "Riedmiller"],
        "year": 2013,
        "doi": "10.48550/arXiv.1312.5602",
        "title": "Playing Atari with deep reinforcement learning",
        "venue": "arXiv preprint"
    },
    # ---- Medicine / Bioinformatics ----
    {
        "id": "GT09",
        "authors": ["LeCun", "Bengio", "Hinton"],
        "year": 2015,
        "doi": "10.1038/nature14539",
        "title": "Deep learning",
        "venue": "Nature"
    },
    {
        "id": "GT10",
        "authors": ["Esteva", "Kuprel", "Novoa", "Ko", "Swetter", "Blau", "Thrun"],
        "year": 2017,
        "doi": "10.1038/nature21056",
        "title": "Dermatologist-level classification of skin cancer with deep neural networks",
        "venue": "Nature"
    },
    # ---- Social Sciences ----
    {
        "id": "GT11",
        "authors": ["Bartlett"],
        "year": 2014,
        "doi": "10.5860/llm.v29i1.7116",
        "title": "New and Noteworthy: Coming to Terms with Librarian Stereotypes and Self-Image",
        "venue": "Library Leadership & Management"
    },
    {
        "id": "GT12",
        "authors": ["Putnam"],
        "year": 1995,
        "doi": "10.1080/00323267.1995.9936422",
        "title": "Bowling Alone: America's Declining Social Capital",
        "venue": "Journal of Democracy"
    },
    # ---- Economics ----
    {
        "id": "GT13",
        "authors": ["Acemoglu", "Johnson", "Robinson"],
        "year": 2001,
        "doi": "10.1257/aer.91.5.1369",
        "title": "The Colonial Origins of Comparative Development: An Empirical Investigation",
        "venue": "American Economic Review"
    },
    {
        "id": "GT14",
        "authors": ["Arrow"],
        "year": 1963,
        "doi": "10.2307/1812352",
        "title": "Uncertainty and the Welfare Economics of Medical Care",
        "venue": "The American Economic Review"
    },
    # ---- Physics ----
    {
        "id": "GT15",
        "authors": ["Einstein", "Podolsky", "Rosen"],
        "year": 1935,
        "doi": "10.1103/PhysRev.47.777",
        "title": "Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?",
        "venue": "Physical Review"
    },
    # ---- Biology ----
    {
        "id": "GT16",
        "authors": ["Watson", "Crick"],
        "year": 1953,
        "doi": "10.1038/171737a0",
        "title": "Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid",
        "venue": "Nature"
    },
    # ---- Computer Science / Algorithms ----
    {
        "id": "GT17",
        "authors": ["Cormen", "Leiserson", "Rivest", "Stein"],
        "year": 2009,
        "doi": "10.5555/1875474",
        "title": "Introduction to Algorithms",
        "venue": "MIT Press"
    },
    # ---- Information Retrieval ----
    {
        "id": "GT18",
        "authors": ["Robertson", "Zaragoza"],
        "year": 2009,
        "doi": "10.1561/1500000019",
        "title": "The Probabilistic Relevance Framework: BM25 and Beyond",
        "venue": "Foundations and Trends in Information Retrieval"
    },
    # ---- Cognitive Science ----
    {
        "id": "GT19",
        "authors": ["Kahneman"],
        "year": 2003,
        "doi": "10.1257/089533003321164987",
        "title": "Maps of Bounded Rationality: Psychology for Behavioral Economics",
        "venue": "American Economic Review"
    },
    # ---- Climate Science ----
    {
        "id": "GT20",
        "authors": ["Hansen", "Ruedy", "Sato", "Lo"],
        "year": 2010,
        "doi": "10.1029/2010RG000345",
        "title": "Global surface temperature change",
        "venue": "Reviews of Geophysics"
    },
    # ---- Linguistics ----
    {
        "id": "GT21",
        "authors": ["Chomsky"],
        "year": 1956,
        "doi": "10.1109/TIT.1956.1056813",
        "title": "Three models for the description of language",
        "venue": "IRE Transactions on Information Theory"
    },
    # ---- Robotics ----
    {
        "id": "GT22",
        "authors": ["Thrun", "Burgard", "Fox"],
        "year": 2005,
        "doi": "10.5555/1121596",
        "title": "Probabilistic Robotics",
        "venue": "MIT Press"
    },
    # ---- Graph Neural Networks ----
    {
        "id": "GT23",
        "authors": ["Kipf", "Welling"],
        "year": 2017,
        "doi": "10.48550/arXiv.1609.02907",
        "title": "Semi-supervised classification with graph convolutional networks",
        "venue": "International Conference on Learning Representations"
    },
    # ---- Generative Models ----
    {
        "id": "GT24",
        "authors": ["Goodfellow", "Pouget-Abadie", "Mirza", "Xu", "Warde-Farley", "Ozair", "Courville", "Bengio"],
        "year": 2014,
        "doi": "10.48550/arXiv.1406.2661",
        "title": "Generative adversarial nets",
        "venue": "Advances in Neural Information Processing Systems"
    },
    # ---- Explainability ----
    {
        "id": "GT25",
        "authors": ["Ribeiro", "Singh", "Guestrin"],
        "year": 2016,
        "doi": "10.1145/2939672.2939778",
        "title": "Why Should I Trust You?: Explaining the Predictions of Any Classifier",
        "venue": "Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining"
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

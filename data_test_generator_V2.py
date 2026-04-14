import random
from typing import List, Dict, Optional

# =============================================================================
# GROUND TRUTH — 25 papers across different domains
# =============================================================================
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

# =============================================================================
# TYPES OF SEMANTIC CORRUPTION
# =============================================================================
CORRUPTION_TYPES = [
    None,             # correct reference
    "title",          # modified title
    "authors",        # added/incorrect author
    "year",           # shifted year
    "metadata_combo", # both title and author incorrect
    "invalid_doi",    # fabricated DOI
    "partial"         # incomplete, non-verifiable citation
]

CORRUPTION_WEIGHTS = [0.30, 0.10, 0.10, 0.10, 0.10, 0.15, 0.15]


# =============================================================================
# PARSING DEGRADATIONS (simulation of Monitor LLM output)
# =============================================================================
PARSING_DEGRADATION_TYPES = [
    "none",           # perfect parsing — optimistic case
    "et_al",          # only first author extracted ("et al." not expanded)
    "missing_title",  # title not extracted (null)
    "truncated_title",# title truncated halfway
    "missing_year",   # year not extracted (null)
]

DEGRADATION_WEIGHTS = [0.55, 0.15, 0.10, 0.10, 0.10]


def apply_parsing_degradation(parsed: Dict, degradation: str) -> Dict:
    """
    Simulates a degraded Monitor LLM output on the 'parsed' field.
    Does not modify the citation text, only the parsed structure
    that the Plan would receive as input.
    """
    result = dict(parsed)

    if degradation == "none":
        return result

    elif degradation == "et_al":
        # The Monitor saw "Krizhevsky et al." and did not expand the list
        if result.get("authors") and len(result["authors"]) > 1:
            result["authors"] = [result["authors"][0]]

    elif degradation == "missing_title":
        result["title"] = None

    elif degradation == "truncated_title":
        if result.get("title"):
            cutoff = max(5, len(result["title"]) // 2)
            result["title"] = result["title"][:cutoff]

    elif degradation == "missing_year":
        result["year"] = None

    return result


# =============================================================================
# SINGLE REFERENCE GENERATION
# =============================================================================
def make_reference(ref: Dict, corruption_type: Optional[str], rng: random.Random) -> Dict:
    """
    Generates a textual citation and the corresponding ideal parsed version
    starting from a ground truth record.

    Returns:
        {
            "text": str,           citation text
            "parsed_ideal": dict,  parsed without degradation
            "label": str           true / corrupt / partial
        }
    """
    authors_str = ", ".join(ref["authors"])
    year = ref["year"]
    title = ref["title"]
    venue = ref["venue"]
    doi = ref["doi"]

    # --- Semantic corruption ---
    if corruption_type == "title":
        title = title.replace("the", "a", 1) + " (misstated title)"
    elif corruption_type == "authors":
        authors_str = authors_str + ", Smith"
    elif corruption_type == "year":
        year = year + rng.choice([-2, -1, 1, 2])
    elif corruption_type == "metadata_combo":
        title = "Modified version of " + title
        authors_str = authors_str.replace(ref["authors"][0], "WrongAuthor")
    elif corruption_type == "invalid_doi":
        doi = "10.fake/" + str(rng.randint(1000, 9999))
    elif corruption_type == "partial":
        text = f"{ref['authors'][0]} ({ref['year']}) mentioned this topic."
        return {
            "text": text,
            "parsed_ideal": {
                "doi": None,
                "authors": [ref["authors"][0]],
                "year": ref["year"],
                "title": None,
                "venue": None
            },
            "label": "partial"
        }

    text = f"{authors_str} ({year}). {title}. {venue}. DOI: {doi}."
    parsed_ideal = {
        "doi": doi,
        "authors": authors_str.split(", "),
        "year": year,
        "title": title,
        "venue": venue
    }

    label = "true" if corruption_type is None else "corrupt"

    return {
        "text": text,
        "parsed_ideal": parsed_ideal,
        "label": label
    }


# =============================================================================
# TEST SET GENERATION
# =============================================================================
def generate_test_references(
    n: int = 300,
    seed: int = 42,
    apply_degradation: bool = True
) -> List[Dict]:
    """
    Generates n synthetic references with controlled corruption and degradation.

    Args:
        n:                  number of citations to generate
        seed:               seed for reproducibility
        apply_degradation:  if True, applies parsing degradations
                            (Monitor output simulation); if False,
                            uses ideal parsed (pure optimistic case)

    Returns:
        List of dicts with keys:
            text, parsed, label, corruption_type, degradation_type
    """
    rng = random.Random(seed)
    results = []

    for _ in range(n):
        ref = rng.choice(GROUND_TRUTH)
        corruption_type = rng.choices(CORRUPTION_TYPES, weights=CORRUPTION_WEIGHTS, k=1)[0]
        degradation_type = (
            rng.choices(PARSING_DEGRADATION_TYPES, weights=DEGRADATION_WEIGHTS, k=1)[0]
            if apply_degradation else "none"
        )

        generated = make_reference(ref, corruption_type, rng)

        # Apply degradation to parsed (only if not partial — already incomplete by definition)
        if generated["label"] != "partial" and degradation_type != "none":
            parsed_degraded = apply_parsing_degradation(generated["parsed_ideal"], degradation_type)
        else:
            parsed_degraded = generated["parsed_ideal"]

        results.append({
            "text": generated["text"],
            "parsed": parsed_degraded,
            "parsed_ideal": generated["parsed_ideal"],
            "label": generated["label"],
            "corruption_type": corruption_type if corruption_type else "none",
            "degradation_type": degradation_type
        })

    return results


# =============================================================================
# SUMMARY
# =============================================================================
def print_generation_summary(refs: List[Dict], seed: int):
    counts = {"true": 0, "corrupt": 0, "partial": 0}
    degradation_counts = {}

    for r in refs:
        counts[r["label"]] += 1
        d = r["degradation_type"]
        degradation_counts[d] = degradation_counts.get(d, 0) + 1

    n = len(refs)
    print(f"\n=== GENERATION SUMMARY (seed={seed}, n={n}) ===")
    print(f"  Correct (true):    {counts['true']}  ({counts['true']/n*100:.1f}%)")
    print(f"  Corrupted (corrupt): {counts['corrupt']}  ({counts['corrupt']/n*100:.1f}%)")
    print(f"  Partial (partial): {counts['partial']}  ({counts['partial']/n*100:.1f}%)")
    print(f"\n  Applied parsing degradations:")
    for d, c in sorted(degradation_counts.items()):
        print(f"    {d:20s}: {c}  ({c/n*100:.1f}%)")


# =============================================================================
# COMPATIBILITY — TEST_REFERENCES used by the benchmark
# =============================================================================
# Default generation: seed=42, n=300, with degradation
TEST_REFERENCES = generate_test_references(n=300, seed=42, apply_degradation=True)


if __name__ == "__main__":
    print_generation_summary(TEST_REFERENCES, seed=42)
    print("\nFirst 5 generated examples:")
    for r in TEST_REFERENCES[:5]:
        print(f"\n  [{r['label'].upper()} | corruption={r['corruption_type']} | degradation={r['degradation_type']}]")
        print(f"  TEXT:   {r['text']}")
        print(f"  PARSED: {r['parsed']}")
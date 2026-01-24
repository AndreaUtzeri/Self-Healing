import json
from typing import List, Dict


def extract_json_block(text: str) -> List[Dict]:
    
    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1:
        print("\n[DEBUG] Raw LLM output without JSON array:\n", text)
        raise ValueError("The LLM output does not contain a JSON array.")

    json_str = text[start:end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("\n[DEBUG] Extracted JSON candidate:\n", json_str)
        raise ValueError(f"Failed to parse JSON from LLM output: {e}")


class CitationMonitorLLM:
    def __init__(self, client):
        self.client = client

    def extract_references(self, text: str) -> List[Dict]:
        """
        Uses an LLM to extract bibliographic references (DOIs, author-year, numeric citations, etc.)
        and returns a structured JSON array. Robust against noisy model output.
        """

        # --- ROLE ---
        system_prompt = (
            "You are a strict citation monitoring agent. "
            "You MUST output only valid JSON and must NOT infer information. "
        )

        # --- EXTRACTION SPECIFICATIONS ---
        extraction_spec = """
            You are a citation monitoring agent.

            TASK:
            Detect *all* bibliographic references in the text, even if incomplete, ambiguous,
            partially incorrect, or not formally structured.

            You must detect references expressed as:
            - DOIs (e.g., https://doi.org/10.1038/nphys1170)
            - Plain DOI mentions (e.g., DOI: 10.1000/xyz123)
            - Numeric citations ([1], [12], etc.)
            - Author–year citations (e.g., Smith et al. 2020)
            - Titles presented as citations
            - Any text fragment that *resembles* a citation, even if malformed or partial

            IMPORTANT RULES:
            AUTHOR EXTRACTION RULES:
            - Extract authors ONLY if their surnames explicitly appear in the text.
            - If a citation is in the form "Lastname et al.", extract only the explicit surname (e.g., ["LeCun"]).
            - If a citation is in the form "Lastname & Lastname", extract both surnames (e.g., ["Ioffe", "Szegedy"]).
            - Do NOT invent or guess missing authors.
            - Do NOT expand “et al.” into full author lists.

            GENERAL RULES:
            - Do NOT infer metadata that is not explicitly present.
            - Extract only what explicitly appears in the text.
            - If a field is not explicitly stated, set it to null.

            - Do NOT rewrite or “clean up” the reference text.

            OUTPUT FORMAT (MANDATORY):

            A single JSON array of objects:

            [
            {
                "id": "ref_01",
                "detected_form": "string",
                "location": { "start": int, "end": int },
                "parsed": {
                    "doi": string | null,
                    "authors": [string] | null,
                    "title": string | null,
                    "year": int | null,
                    "venue": string | null
                },
                "context": "string"
            }
            ]

            RESTRICTIONS:
            - Your final answer MUST start with '[' and end with ']'.
            - No explanations, no markdown, no text outside the JSON array.
            - If you include text outside the JSON, the system will fail.
            """

        prompt = f"{extraction_spec}\n\nTEXT TO ANALYZE:\n{text}"

        
        raw_output = self.client.generate_text(system_prompt, prompt)
        output_text = raw_output["text"]

        

        
        structured_output = extract_json_block(output_text)

        return structured_output

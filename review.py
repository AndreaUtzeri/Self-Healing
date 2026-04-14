from api_openai import OpenAIClient
import re

class CitationRefiner:
    def __init__(self, client):
        self.client = client

    # --------------------------------------------------------------
    # 1. Reconstruct correct citation based on Crossref
    # --------------------------------------------------------------
    def refine_sentence(self, sentence: str) -> str:
        """Corrects the syntax of a single sentence containing [[OMIT]] placeholders."""
        content = (
            "You are an assistant that corrects grammar and syntax of academic texts. "
            
        )

        prompt = (
            f"Rewrite this sentence to be grammatically correct and fluent, "
            f"removing the [[OMIT]] placeholders and reformulating the sentence after their removal:\n\n{sentence}"
        )

        refined = self.client.generate_text(content, prompt)
        return refined.strip()

    # --------------------------------------------------------------
    # Optimized version: batch processing of sentences with [[OMIT]]
    # --------------------------------------------------------------
    def refine_text(self, text: str) -> str:
        """
        Optimized version:
        - Extracts all sentences containing [[OMIT]].
        - Removes duplicates.
        - Sends them all together in a single call to the model.
        - Reconstructs the text by replacing only the corrected sentences.
        """
        print("\n=== DEBUG: Refining by context (optimized) ===")

        # Split the text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        print(f"Sentences found: {len(sentences)}")

        # Filter only sentences that contain [[OMIT]]
        sentences_to_refine = [s for s in sentences if "[[OMIT]]" in s]
        sentences_to_refine = list(set(sentences_to_refine))  # remove duplicates

        if not sentences_to_refine:
            print("[DEBUG] No sentences to refine.")
            return text

        print(f"Sentences to send to the model: {len(sentences_to_refine)}")

        # Prepare unified prompt
        content = (
            "You are an assistant that corrects grammar and syntax of academic texts. "
            "Remove the [[OMIT]] placeholders and reformulate the sentences in a fluent and coherent way. "
            "Return the corrected sentences in the same order, separated by '---'."
        )

        joined_sentences = "\n---\n".join(sentences_to_refine)
        prompt = f"Here are the sentences to correct:\n\n{joined_sentences}"

        # Single call to the model
        refined_block = self.client.generate_text(content, prompt)["text"]
        refined_sentences = [s.strip() for s in refined_block.split('---') if s.strip()]

        # Check that the number of sentences matches
        if len(refined_sentences) != len(sentences_to_refine):
            print("[WARNING] The number of corrected sentences does not match the original. "
                  "There may be minor alignment discrepancies.")

        # Reconstruct the final text
        final_text = text
        for original, refined in zip(sentences_to_refine, refined_sentences):
            final_text = final_text.replace(original, refined)

        result = self.client.generate_text(content, prompt)
        print("[DEBUG] Review completed (full text)")
        return result["text"], result  # return text + metrics
    
    # Alternative version: refine the entire text in one go (less control, but simpler)
    
    def refine_full_text(self, text: str) -> str:
        
        content = (
            "You are an assistant that corrects grammar and syntax of academic texts. "
            "The text may contain [[OMIT]] placeholders representing removed citations."
        )

        prompt = (
            f"Rewrite the following text to be grammatically correct and coherent, "
            f"without changing its content, but removing the [[OMIT]] placeholders:\n\n{text}"
        )

        result = self.client.generate_text(content, prompt)
        print("[DEBUG] Review completed (full text)")
        return result["text"], result 
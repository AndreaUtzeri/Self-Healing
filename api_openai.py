from openai import OpenAI
import time

class OpenAIClient:
    def __init__(self, model: str ="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate_text(self, content: str ,prompt: str) -> str:
        

        start_time = time.time()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        latency = time.time() - start_time
        usage = response.usage

        cost = (usage.prompt_tokens / 1000) * 0.00015 + (usage.completion_tokens / 1000) * 0.0006

        result = {
            "text": response.choices[0].message.content.strip(),
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "cost": cost,
            "latency": latency,
        }

        return result

       
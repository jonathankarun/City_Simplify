import openai

class OpenAIClient:
    def __init__(self):
        openai.api_key = "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"

    def generate_answer(self, question: str, context: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Context: {context}\nQuestion: {question}\nAnswer:",
            max_tokens=150
        )
        return response.choices[0].text.strip()

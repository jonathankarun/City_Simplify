import openai

class OpenAIClient:
    def __init__(self):
        openai.api_key = "My_OpenAI_key"

    def generate_answer(self, question: str, context: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Context: {context}\nQuestion: {question}\nAnswer:",
            max_tokens=150
        )
        return response.choices[0].text.strip()

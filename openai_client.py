#Imports
import os
import openai
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        # Set your OpenAI API key here
        openai.api_key = "OPENAI-KEY"

    #Generate answer function
    def generate_answer(self, question: str, context: str) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Context: {context}\nQuestion: {question}\nAnswer:",
            max_tokens=150
        )
        return response.choices[0].text.strip()

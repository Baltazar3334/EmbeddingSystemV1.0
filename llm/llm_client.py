"""
Ollama LLM client.
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "phi3:mini"


# GENERATE ================================================
def generate(prompt: str) -> str:

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]
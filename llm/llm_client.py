"""
Ollama LLM client.
"""

import requests

from config import(
MODEL_NAME_LLM
)

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = MODEL_NAME_LLM


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
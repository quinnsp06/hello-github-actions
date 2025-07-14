# ai_helper/explain_error.py

import os
import sys
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

log = sys.stdin.read()

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-70b-8192",
    "messages": [
        {
            "role": "system",
            "content": "Análise de erro de Código"
        },
        {
            "role": "user",
            "content": f"O seguinte erro aconteceu durante uma etapa do build:\n\n{log}\n\nExplique o que deu errado e sugira como corrigir."
        }
    ],
    "temperature": 0.2
}

response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
print(response.json()['choices'][0]['message']['content'])

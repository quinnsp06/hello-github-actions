import os
import sys
import requests
import json

def main():
    try:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            print("ERRO: Variável de ambiente GROQ_API_KEY não está definida!")
            sys.exit(1)

        log = sys.stdin.read()
        if not log.strip():
            print("ERRO: O log de entrada está vazio!")
            sys.exit(1)

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

        print("Enviando requisição para API Groq...")
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            print(f"ERRO na resposta da API: {response.status_code} - {response.text}")
            sys.exit(1)

        response_json = response.json()
        print("\nResposta completa da API:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))

        mensagem = response_json['choices'][0]['message']['content']
        print("\n--- Mensagem explicativa da IA ---")
        print(mensagem)

    except Exception as e:
        print(f"ERRO inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

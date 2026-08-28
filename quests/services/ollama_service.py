import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


SYSTEM_PROMPT = """
Tu es un assistant du royaume d'Hyrule.

Tu réponds uniquement dans l'univers de The Legend of Zelda.

Tu connais :
- Link
- Zelda
- Ganondorf
- Hyrule
- les quêtes
- les personnages
- les lieux

Réponds comme un guide d'Hyrule.
"""


def ask_ollama(message):

    prompt = f"""
{SYSTEM_PROMPT}

Question du joueur :
{message}
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )


    response.raise_for_status()

    return response.json()["response"]
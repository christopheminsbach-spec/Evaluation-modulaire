"""
Service Chatbot Zelda
Communication avec Ollama local
"""

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3.2:3b"


def ask_ollama(question, context=None):
    """
    Envoie une question au modèle Ollama
    """

    prompt = build_chat_prompt(
        question,
        context
    )


    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }


    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )


        response.raise_for_status()


        data = response.json()


        return data.get(
            "response",
            "Le sage d'Hyrule reste silencieux..."
        )


    except requests.exceptions.RequestException:

        return (
            "Impossible de contacter "
            "le gardien d'Hyrule."
        )



def build_chat_prompt(question, context=None):

    base = """
Tu es Navi, le guide du royaume d'Hyrule.

Règles :
- Tu réponds uniquement dans l'univers Zelda.
- Tu connais Link, Zelda, Ganondorf, Hyrule.
- Tu restes dans un rôle médiéval fantastique.
- Tu aides les aventuriers.

"""


    if context:
        base += f"""
Contexte :
{context}
"""


    base += f"""

Question du héros :

{question}

Réponse :
"""


    return base
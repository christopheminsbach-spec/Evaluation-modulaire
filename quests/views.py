
import json

import requests

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Location, Quest
from .services.spellcheck_service import correct_text


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

def home(request):

    total = Quest.objects.count()

    available = Quest.objects.filter(
        completed=False
    ).count()

    completed = Quest.objects.filter(
        completed=True
    ).count()

    total_rewards = sum(
        Quest.objects.values_list(
            "reward",
            flat=True
        )
    )

    context = {
        "total": total,
        "available": available,
        "completed": completed,
        "total_rewards": total_rewards,
    }

    return render(
        request,
        "home.html",
        context
    )


# ============================================================
# LISTE DES QUÊTES
# ============================================================

def quest_list(request):

    quests = Quest.objects.select_related(
        "location"
    ).all()

    status = request.GET.get("status")

    if status == "available":

        quests = quests.filter(
            completed=False
        )

    elif status == "completed":

        quests = quests.filter(
            completed=True
        )

    context = {
        "quests": quests,
        "current_status": status,
    }

    return render(
        request,
        "quests/quest_list.html",
        context
    )


# ============================================================
# DETAIL D'UNE QUÊTE
# ============================================================

def quest_detail(request, id):

    quest = get_object_or_404(
        Quest.objects.select_related(
            "location"
        ),
        id=id
    )

    return render(
        request,
        "quests/quest_detail.html",
        {
            "quest": quest
        }
    )


# ============================================================
# LISTE DES LIEUX
# ============================================================

def location_list(request):

    locations = Location.objects.all()

    return render(
        request,
        "quests/location_list.html",
        {
            "locations": locations
        }
    )


# ============================================================
# DETAIL D'UN LIEU
# ============================================================

def location_detail(request, id):

    location = get_object_or_404(
        Location,
        id=id
    )

    available_quests = Quest.objects.filter(
        location=location,
        completed=False
    )

    completed_quests = Quest.objects.filter(
        location=location,
        completed=True
    )

    return render(
        request,
        "quests/location_detail.html",
        {
            "location": location,
            "available_quests": available_quests,
            "completed_quests": completed_quests,
        }
    )


# ============================================================
# CHATBOT ZELDA — PAGE
# ============================================================

def chat(request):

    return render(
        request,
        "quests/chat.html"
    )


# ============================================================
# CHATBOT ZELDA — API
# ============================================================

@require_POST
def chat_api(request):

    # --------------------------------------------------------
    # 1. Lecture du JSON
    # --------------------------------------------------------

    try:

        data = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "JSON invalide"
            },
            status=400
        )


    # --------------------------------------------------------
    # 2. Récupération du message
    # --------------------------------------------------------

    message = data.get(
        "message",
        ""
    ).strip()


    if not message:

        return JsonResponse(
            {
                "error": "Message vide"
            },
            status=400
        )


    # --------------------------------------------------------
    # 3. Correction orthographique
    # --------------------------------------------------------

    corrected_message = correct_text(
        message
    )

    print("==========================")
    print("Question originale :", message)
    print("Question corrigée  :", corrected_message)
    print("==========================")


    # --------------------------------------------------------
    # 4. Prompt système Zelda
    # --------------------------------------------------------

    system_prompt = """
Tu es Hyrule Guide.

Tu réponds uniquement dans l'univers
de The Legend of Zelda.

Tu es spécialisé dans :

- Link
- Zelda
- Ganondorf
- Hyrule
- personnages
- lieux
- objets
- créatures
- histoire de Zelda

Réponds toujours en français.

Si la question ne concerne pas Zelda,
explique que tu es uniquement un guide
d'Hyrule.

Réponds de manière courte, claire
et utile.
"""


    # --------------------------------------------------------
    # 5. Création du prompt
    # --------------------------------------------------------

    prompt = f"""
{system_prompt}

Question du joueur :

{corrected_message}

Réponse :
"""


    # --------------------------------------------------------
    # 6. Communication avec Ollama
    # --------------------------------------------------------

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "llama3.2:3b",

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.4,

                    "num_predict": 150

                }

            },

            timeout=120
        )

        response.raise_for_status()


    except requests.exceptions.RequestException as e:

        print(
            "Erreur Ollama :",
            str(e)
        )

        return JsonResponse(
            {
                "error": f"Erreur Ollama : {str(e)}"
            },
            status=503
        )


    # --------------------------------------------------------
    # 7. Lecture de la réponse Ollama
    # --------------------------------------------------------

    try:

        ollama_data = response.json()

    except ValueError:

        return JsonResponse(
            {
                "error": "Réponse Ollama invalide"
            },
            status=503
        )


    answer = ollama_data.get(
        "response",
        ""
    ).strip()


    # --------------------------------------------------------
    # 8. Réponse JSON au frontend
    # --------------------------------------------------------

    return JsonResponse(
        {
            "question_originale": message,
            "question_corrigee": corrected_message,
            "answer": answer
        }
    )


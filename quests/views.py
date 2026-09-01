import json

import requests

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Location, Quest


def correct_text(text):
    """Corrige le texte en français si LanguageTool est disponible."""
    try:
        import language_tool_python

        tool = language_tool_python.LanguageTool("fr")
        corrected = language_tool_python.utils.correct(
            text,
            tool.check(text)
        )
        tool.close()
        return corrected
    except (ImportError, Exception):
        return text




# ==========================================
# PAGE D'ACCUEIL
# ==========================================

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


# ==========================================
# LISTE DES QUÊTES
# ==========================================

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

    return render(
        request,
        "quests/quest_list.html",
        {
            "quests": quests,
            "current_status": status,
        }
    )


# ==========================================
# DETAIL D'UNE QUÊTE
# ==========================================

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


# ==========================================
# LISTE DES LIEUX
# ==========================================

def location_list(request):

    locations = Location.objects.all()

    return render(
        request,
        "quests/location_list.html",
        {
            "locations": locations
        }
    )


# ==========================================
# DETAIL D'UN LIEU
# ==========================================

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


# ==========================================
# PAGE CHAT
# ==========================================

def chat(request):

    # --------------------------------------
    # AFFICHAGE DE LA PAGE
    # --------------------------------------

    if request.method == "GET":

        return render(
            request,
            "quests/chat.html"
        )

from django.views.decorators.http import require_POST
import json

from .services.spellcheck_service import correct_text


@require_POST
def chat_api(request):

    try:

        data = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "JSON invalide"
            },
            status=405
        )


    message = request.POST.get(
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



    corrected = correct_text(
        message
    )


    prompt = f"""

Tu es Hyrule Guide.

Tu réponds uniquement
dans l'univers de Zelda.

Question :

{corrected}

Réponse :

"""


    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "llama3.2:3b",

                "prompt": prompt,

                "stream": False

            },

            timeout=120

        )


        response.raise_for_status()


    except requests.exceptions.RequestException as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=503
        )



    result = response.json()


    return JsonResponse(
        {
            "question_corrigee": corrected,
            "answer": result.get(
                "response",
                ""
            )
        }
    )


    # ======================================
    # CORRECTION ORTHOGRAPHIQUE
    # ======================================

    corrected_message = correct_text(
        message
    )



    print(
        "Question originale :",
        message
    )


    print(
        "Question corrigée :",
        corrected_message
    )



    # ======================================
    # PROMPT ZELDA
    # ======================================

    system_prompt = """

Tu es Hyrule Guide.

Tu réponds uniquement
dans l'univers de The Legend of Zelda.

Tu es spécialisé dans :

- Link
- Zelda
- Ganondorf
- Hyrule
- personnages
- lieux
- objets
- créatures
- histoire Zelda

RÈGLES :

1. Réponds toujours en français.

Si la question ne concerne pas Zelda,
explique que tu es uniquement
un guide d'Hyrule.

Réponse courte et claire.

"""



    prompt = f"""
{system_prompt}


Question du joueur :

{corrected_message}


Réponse :

"""



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


        return JsonResponse(
            {
                "error":
                f"Erreur Ollama : {str(e)}"
            },

            status=503

        )



    data = response.json()



    answer = ollama_data.get(
        "response",
        ""
    ).strip()



    return JsonResponse(
        {

            "question_originale":
                message,

            "question_corrigee":
                corrected_message,

            "answer":
                answer

        }
    )


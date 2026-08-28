import requests

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Location, Quest


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

    context = {
        "quests": quests,
        "current_status": status,
    }

    return render(
    request,
    "quests/quest_list.html",
    {
        "quests": quests
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
# CHATBOT ZELDA
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

    # --------------------------------------
    # VÉRIFICATION DE LA MÉTHODE
    # --------------------------------------

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Méthode non autorisée."
            },
            status=405
        )

    # --------------------------------------
    # RÉCUPÉRATION DU MESSAGE
    # --------------------------------------

    message = request.POST.get(
        "message",
        ""
    ).strip()

    if not message:

        return JsonResponse(
            {
                "error": "Veuillez écrire une question."
            },
            status=400
        )

    # ======================================
    # PROMPT SYSTÈME
    # ======================================

    system_prompt = """
Tu es Hyrule Guide, un assistant spécialisé
dans l'univers de The Legend of Zelda.

Tu réponds uniquement aux questions concernant
l'univers Zelda.

Tu peux parler de :

- Link
- Zelda
- Ganondorf
- Hyrule
- les jeux Zelda
- les personnages
- les peuples
- les créatures
- les objets
- les armes
- les donjons
- les sanctuaires
- les quêtes
- les lieux
- la chronologie
- la mythologie
- l'histoire de Zelda

RÈGLES :

1. Réponds toujours en français.

2. Reste dans l'univers de Zelda.

3. Si la question n'a aucun rapport avec Zelda,
indique simplement que tu es spécialisé dans
l'univers de Zelda.

4. Ne réponds pas aux questions concernant :
programmation, Django, Python, politique,
actualité, médecine, droit ou autres jeux vidéo.

5. Ne prétends jamais être un personnage officiel
de Zelda.

6. Si une information varie selon les jeux,
explique-le clairement.

7. Donne des réponses courtes et faciles à comprendre.

8. Ne fais pas de longue réflexion visible.

9. Ne répète pas la question de l'utilisateur.

10. Réponds directement à la question.

Tu es le guide des aventuriers d'Hyrule.
"""

    # ======================================
    # PROMPT
    # ======================================

    prompt = f"""
{system_prompt}

Question :

{message}

Réponse :
"""

    # ======================================
    # APPEL À OLLAMA
    # ======================================

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={
                "model": "gemma3:1b",
                "prompt": prompt,
                "stream": False,

                "options": {
                    "temperature": 0.4,
                    "num_predict": 150
                }
            },

            timeout=120
        )

    except requests.exceptions.ConnectionError:

        return JsonResponse(
            {
                "error": (
                    "Impossible de contacter Ollama. "
                    "Vérifiez qu'Ollama est lancé."
                )
            },
            status=503
        )

    except requests.exceptions.Timeout:

        return JsonResponse(
            {
                "error": (
                    "Ollama met trop de temps à répondre."
                )
            },
            status=504
        )

    except requests.exceptions.RequestException as e:

        return JsonResponse(
            {
                "error": f"Erreur de connexion à Ollama : {str(e)}"
            },
            status=500
        )

    # ======================================
    # VÉRIFICATION DE LA RÉPONSE HTTP
    # ======================================

    if response.status_code != 200:

        return JsonResponse(
            {
                "error": (
                    "Ollama a retourné une erreur : "
                    f"{response.text}"
                )
            },
            status=500
        )

    # ======================================
    # CONVERSION JSON
    # ======================================

    try:

        data = response.json()

    except ValueError:

        return JsonResponse(
            {
                "error": (
                    "Ollama a retourné une réponse "
                    "qui n'est pas du JSON."
                )
            },
            status=500
        )

    # ======================================
    # DEBUG
    # ======================================

    print("\n========== OLLAMA ==========")
    print("Modèle :", data.get("model"))
    print("Réponse :", data.get("response"))
    print("Done :", data.get("done"))
    print("============================\n")

    # ======================================
    # RÉCUPÉRATION DE LA RÉPONSE
    # ======================================

    answer = data.get(
        "response",
        ""
    )

    if answer is None:
        answer = ""

    answer = answer.strip()

    # ======================================
    # AUCUNE RÉPONSE
    # ======================================

    if not answer:

        return JsonResponse(
            {
                "error": (
                    "Ollama n'a fourni aucune réponse."
                )
            },
            status=500
        )

    # ======================================
    # RÉPONSE AU FRONTEND
    # ======================================

    return JsonResponse(
        {
            "answer": answer
        }
    )
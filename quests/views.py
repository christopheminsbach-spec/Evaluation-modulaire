import requests

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Location, Quest


# ==========================================
# PAGE D'ACCUEIL
# ==========================================

def home(request):

    # Nombre total de quêtes
    total = Quest.objects.count()

    # Quêtes encore disponibles
    available = Quest.objects.filter(
        completed=False
    ).count()

    # Quêtes terminées
    completed = Quest.objects.filter(
        completed=True
    ).count()

    # Total des récompenses
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

    # Récupération des quêtes
    # select_related évite des requêtes SQL inutiles
    quests = Quest.objects.select_related(
        "location"
    ).all()

    # Récupération du filtre dans l'URL
    status = request.GET.get("status")

    # Filtre : disponibles
    if status == "available":

        quests = quests.filter(
            completed=False
        )

    # Filtre : terminées
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

    # Affichage initial de la page
    if request.method == "GET":

        return render(
            request,
            "quests/chat.html"
        )

    # Vérification de la méthode HTTP
    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Méthode non autorisée."
            },
            status=405
        )

    # Récupération du message envoyé
    message = request.POST.get(
        "message",
        ""
    ).strip()

    # Vérification du message
    if not message:

        return JsonResponse(
            {
                "error": "Veuillez écrire une question."
            },
            status=400
        )

    # ======================================
    # CONSIGNE SYSTÈME
    # ======================================

    system_prompt = """
Tu es Hyrule Guide, un assistant spécialisé
exclusivement dans l'univers de The Legend of Zelda.

Ta mission est de répondre aux questions concernant :

- les jeux The Legend of Zelda
- les personnages
- les lieux
- les peuples
- les créatures
- les objets
- les armes
- les donjons
- les sanctuaires
- les quêtes
- la chronologie
- la mythologie
- l'histoire de l'univers Zelda

Règles obligatoires :

1. Tu dois rester dans l'univers de Zelda.

2. Si l'utilisateur pose une question sans rapport
avec Zelda, réponds poliment que tu es uniquement
un assistant spécialisé dans l'univers de Zelda.

3. Ne réponds pas aux demandes concernant :
   - la programmation
   - Django
   - Python
   - les mathématiques
   - la politique
   - l'actualité
   - les conseils médicaux
   - les conseils juridiques
   - les autres jeux vidéo sans rapport avec Zelda

4. Ne prétends pas être un personnage officiel de Zelda.

5. Si une information est incertaine ou varie selon
les jeux, précise-le.

6. Réponds en français.

7. Sois clair, sympathique et relativement concis.

8. Tu peux utiliser des emojis liés à Zelda lorsque
cela améliore la réponse.

Tu es le guide des aventuriers d'Hyrule.
"""

    # ======================================
    # PROMPT ENVOYÉ À OLLAMA
    # ======================================

    prompt = f"""
{system_prompt}

Question de l'utilisateur :

{message}

Réponds maintenant en français.
"""

    # ======================================
    # APPEL À OLLAMA
    # ======================================

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

    # ======================================
    # ERREUR OLLAMA
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
    # RÉCUPÉRATION DE LA RÉPONSE
    # ======================================

    data = response.json()

    answer = data.get(
        "response",
        ""
    ).strip()

    if not answer:

        return JsonResponse(
            {
                "error": "Ollama n'a fourni aucune réponse."
            },
            status=500
        )

    return JsonResponse(
        {
            "answer": answer
        }
    )
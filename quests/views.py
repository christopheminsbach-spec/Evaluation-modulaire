import json
import requests

from django.shortcuts import (
    render,
    get_object_or_404
)

from django.http import (
    JsonResponse,
    FileResponse
)

from django.views.decorators.http import (
    require_POST,
    require_GET
)


from .models import (
    Location,
    Quest,
    ChatConversation,
    ChatMessage,
)


from .services.question_service import (
    get_questions,
    get_question,
    get_categories,
    get_questions_by_category,
)


from .services.rag_service import (
    build_context
)


from .services.prompt_service import (
    build_zelda_prompt
)


from .services.pdf_service import (
    create_chat_pdf
)


try:
    from .services.spellcheck_service import correct_text

except ImportError:

    def correct_text(text):
        return text



# =====================================================
# EXPORT PDF CHAT
# =====================================================

def export_chat_pdf(request, id):

    conversation = get_object_or_404(
        ChatConversation,
        id=id
    )


    pdf_path = create_chat_pdf(
        conversation
    )


    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename=f"hyrule_chat_{id}.pdf"
    )



# =====================================================
# QUESTIONS ZELDA API
# =====================================================

@require_GET
def zelda_questions(request):

    questions = get_questions()


    return JsonResponse({

        "count": len(questions),

        "questions": questions

    })



@require_GET
def zelda_question_detail(request, question_id):

    question = get_question(
        question_id
    )


    if question is None:

        return JsonResponse(
            {
                "error": "Question introuvable"
            },
            status=404
        )


    return JsonResponse(
        question
    )



@require_GET
def zelda_question_categories(request):

    categories = get_categories()


    return JsonResponse({

        "count": len(categories),

        "categories": categories

    })



@require_GET
def zelda_questions_category(request, category):

    questions = get_questions_by_category(
        category
    )


    return JsonResponse({

        "category": category,

        "count": len(questions),

        "questions": questions

    })



# =====================================================
# ACCUEIL
# =====================================================

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


    return render(
        request,
        "home.html",
        {
            "total": total,
            "available": available,
            "completed": completed,
            "total_rewards": total_rewards,
        }
    )



# =====================================================
# QUETES
# =====================================================

def quest_list(request):

    quests = Quest.objects.select_related(
        "location"
    ).all()


    status = request.GET.get(
        "status"
    )


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



# =====================================================
# LOCATIONS
# =====================================================

def location_list(request):

    locations = Location.objects.all()


    return render(
        request,
        "quests/location_list.html",
        {
            "locations": locations
        }
    )



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



# =====================================================
# CHAT HYRULE
# =====================================================

def chat(request):

    return render(
        request,
        "quests/chat.html"
    )



# =====================================================
# CHAT CLASSIQUE
# =====================================================

def chat_classique(request):

    session_key = request.session.session_key


    if not session_key:

        request.session.create()

        session_key = request.session.session_key



    conversation = (
        ChatConversation.objects
        .filter(
            session_key=session_key
        )
        .order_by("-updated_at")
        .first()
    )


    if conversation is None:

        conversation = ChatConversation.objects.create(
            session_key=session_key,
            title="Nouvelle aventure Hyrule"
        )


    messages = conversation.messages.all()



    return render(
        request,
        "quests/chat_classique.html",
        {
            "conversation": conversation,
            "messages": messages,
        }
    )
# =====================================================
# API CHAT HYRULE AVEC MEMOIRE + RAG
# =====================================================

@require_POST
def chat_classique_api(request):

    try:

        data = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "JSON invalide."
            },
            status=400
        )


    message = data.get(
        "message",
        ""
    ).strip()



    if not message:

        return JsonResponse(
            {
                "error": "Message vide."
            },
            status=400
        )



    # =====================================
    # CORRECTION ORTHOGRAPHIQUE
    # =====================================

    try:

        corrected_message = correct_text(
            message
        )

    except Exception:

        corrected_message = message



    # =====================================
    # SESSION UTILISATEUR
    # =====================================

    session_key = request.session.session_key


    if not session_key:

        request.session.create()

        session_key = request.session.session_key



    conversation_id = data.get(
        "conversation_id"
    )



    if conversation_id:


        conversation = get_object_or_404(
            ChatConversation,
            id=conversation_id,
            session_key=session_key
        )


    else:


        conversation = (
            ChatConversation.objects
            .filter(
                session_key=session_key
            )
            .order_by(
                "-updated_at"
            )
            .first()
        )


        if conversation is None:


            conversation = ChatConversation.objects.create(
                session_key=session_key,
                title=message[:150]
            )



    # =====================================
    # SAUVEGARDE QUESTION
    # =====================================

    ChatMessage.objects.create(
        conversation=conversation,
        role="user",
        content=message
    )



    # =====================================
    # MEMOIRE CONVERSATION
    # =====================================

    history = (
        conversation.messages
        .all()
    )


    conversation_text = ""


    for item in history:


        conversation_text += (
            f"{item.role} : "
            f"{item.content}\n"
        )



    # =====================================
    # RAG ZELDA
    # =====================================

    try:

        context = build_context(
            corrected_message
        )


    except Exception:


        context = ""



    # =====================================
    # PROMPT FINAL
    # =====================================

    prompt = build_zelda_prompt(
        question=corrected_message,
        context=context,
        history=conversation_text
    )



    # =====================================
    # APPEL OLLAMA
    # =====================================

    try:


        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model":
                    "llama3.2:3b",


                "prompt":
                    prompt,


                "stream":
                    False,


                "options": {

                    "temperature":
                        0.3,


                    "num_predict":
                        250,

                },

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



    # =====================================
    # REPONSE OLLAMA
    # =====================================

    try:


        ollama_data = response.json()



    except ValueError:


        return JsonResponse(

            {

                "error":
                    "Réponse Ollama invalide."

            },

            status=503

        )




    answer = ollama_data.get(
        "response",
        ""
    ).strip()



    if not answer:


        answer = (
            "Le Guide d'Hyrule "
            "n'a pas trouvé de réponse."
        )



    # =====================================
    # SAUVEGARDE REPONSE
    # =====================================

    ChatMessage.objects.create(

        conversation=conversation,

        role="assistant",

        content=answer

    )



    conversation.save()



    # =====================================
    # RETOUR FRONTEND + PDF
    # =====================================

    return JsonResponse(

        {

            "conversation_id":
                conversation.id,


            "question":
                message,


            "question_corrigee":
                corrected_message,


            "answer":
                answer

        }

    )
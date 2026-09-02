from django.urls import path

from . import views


urlpatterns = [

    # ==========================
    # ACCUEIL
    # ==========================

    path(
        "",
        views.home,
        name="home"
    ),


    # ==========================
    # QUETES
    # ==========================

    path(
        "quests/",
        views.quest_list,
        name="quest_list"
    ),

    path(
        "quests/<int:id>/",
        views.quest_detail,
        name="quest_detail"
    ),


    # ==========================
    # LOCATIONS
    # ==========================

    path(
        "locations/",
        views.location_list,
        name="location_list"
    ),

    path(
        "locations/<int:id>/",
        views.location_detail,
        name="location_detail"
    ),


    # ==========================
    # CHAT HYRULE
    # ==========================

    path(
        "chat/",
        views.chat,
        name="chat"
    ),


    # ==========================
    # CHAT CLASSIQUE
    # ==========================

    path(
        "chat/classique/",
        views.chat_classique,
        name="chat_classique"
    ),


    # ==========================
    # API CHAT CLASSIQUE
    # RAG + MEMOIRE + OLLAMA
    # ==========================

    path(
        "chat/api/",
        views.chat_classique_api,
        name="chat_classique_api"
    ),


    # ==========================
    # QUESTIONS ZELDA
    # ==========================

    path(
        "api/zelda-questions/",
        views.zelda_questions,
        name="zelda_questions"
    ),


    path(
        "api/zelda-questions/<int:question_id>/",
        views.zelda_question_detail,
        name="zelda_question_detail"
    ),


    path(
        "api/zelda-categories/",
        views.zelda_question_categories,
        name="zelda_question_categories"
    ),


    path(
        "api/zelda-category/<str:category>/",
        views.zelda_questions_category,
        name="zelda_questions_category"
    ),


    # ==========================
    # EXPORT PDF
    # ==========================

    path(
        "chat/pdf/<int:id>/",
        views.export_chat_pdf,
        name="export_chat_pdf"
    ),

]
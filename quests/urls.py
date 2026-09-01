
from django.urls import path

from . import views


urlpatterns = [

    # ==========================================
    # ACCUEIL
    # ==========================================

    path(
        "",
        views.home,
        name="home"
    ),


    # ==========================================
    # QUÊTES
    # ==========================================

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


    # ==========================================
    # LIEUX
    # ==========================================

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


    # ==========================================
    # CHAT ZELDA
    # ==========================================

    path(
        "chat/",
        views.chat,
        name="chat"
    ),

    path(
        "chat/api/",
        views.chat_api,
        name="chat_api"
    ),


    # ==========================================
    # CHAT CLASSIQUE
    # ==========================================

    path(
        "chat/classique/",
        views.chat_classique,
        name="chat_classique"
    ),

    path(
        "chat/classique/api/",
        views.chat_classique_api,
        name="chat_classique_api"
    ),


    # ==========================================
    # QUESTIONS JSON ZELDA
    # ==========================================

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
        "api/zelda-questions/categories/",
        views.zelda_question_categories,
        name="zelda_question_categories"
    ),

    path(
        "api/zelda-questions/category/<str:category>/",
        views.zelda_questions_category,
        name="zelda_questions_category"
    ),


    # ==========================================
    # EXPORT PDF DES DISCUSSIONS
    # ==========================================

    path(
        "chat/export/<int:id>/",
        views.export_chat_pdf,
        name="export_chat_pdf"
    ),

]


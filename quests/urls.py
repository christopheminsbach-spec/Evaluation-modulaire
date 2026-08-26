from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "quests/",
        views.quest_list,
        name="quest_list"
    ),

    path(
        "quest/<int:id>/",
        views.quest_detail,
        name="quest_detail"
    ),

    path(
        "locations/",
        views.location_list,
        name="location_list"
    ),

    path(
        "location/<int:id>/",
        views.location_detail,
        name="location_detail"
    ),

    # Chatbot Zelda
    path(
        "chat/",
        views.chat,
        name="chat"
    ),

]
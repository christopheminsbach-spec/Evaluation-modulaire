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
        "quests/<int:id>/",
        views.quest_detail,
        name="quest_detail"
    ),

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

]
from django.contrib import admin

from .models import Location, Quest



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "region"
    )



@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):

    list_display = (

        "title",
        "difficulty",
        "reward",
        "completed",
        "location"

    )


    list_filter = (

        "completed",
        "difficulty"

    )
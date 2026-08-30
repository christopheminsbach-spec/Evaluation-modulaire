
from django.db import models


# ==========================================
# LIEU D'HYRULE
# ==========================================

class Location(models.Model):

    name = models.CharField(
        max_length=100
    )

    region = models.CharField(
        max_length=100
    )

    character = models.CharField(
        max_length=100,
        default="villager.png"
    )

    map_image = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    marker_x = models.FloatField(
        default=50
    )

    marker_y = models.FloatField(
        default=50
    )

    def __str__(self):
        return self.name


# ==========================================
# QUÊTE
# ==========================================

DIFFICULTY = (
    ("easy", "Facile"),
    ("medium", "Moyenne"),
    ("hard", "Difficile"),
)


class Quest(models.Model):

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY
    )

    reward = models.IntegerField()

    completed = models.BooleanField(
        default=False
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="quests"
    )

    def __str__(self):
        return self.title


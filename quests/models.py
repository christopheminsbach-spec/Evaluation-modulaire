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


# ==========================================
# CONVERSATION DU CHAT CLASSIQUE
# ==========================================

class ChatConversation(models.Model):

    session_key = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=150,
        default="Nouvelle conversation"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


# ==========================================
# MESSAGE DU CHAT CLASSIQUE
# ==========================================

class ChatMessage(models.Model):

    ROLE_CHOICES = (
        ("user", "Utilisateur"),
        ("assistant", "Assistant"),
    )

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role} - {self.created_at}"
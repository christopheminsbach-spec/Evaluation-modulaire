from pathlib import Path

from django.conf import settings

from reportlab.platypus import (  # type: ignore
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet  # type: ignore

def create_chat_pdf(conversation):

    folder = Path(
        settings.MEDIA_ROOT
    ) / "conversations"


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        folder /
        f"hyrule_chat_{conversation.id}.pdf"
    )


    document = SimpleDocTemplate(
        str(filename)
    )


    styles = getSampleStyleSheet()


    elements = []


    elements.append(
        Paragraph(
            "Guide d'Hyrule",
            styles["Title"]
        )
    )


    elements.append(
        Spacer(1,20)
    )


    elements.append(
        Paragraph(
            f"Conversation {conversation.id}",
            styles["Heading2"]
        )
    )


    elements.append(
        Spacer(1,20)
    )


    for message in conversation.messages.all():


        role = (
            "Joueur"
            if message.role == "user"
            else
            "Guide d'Hyrule"
        )


        text = (
            f"<b>{role}</b><br/>"
            f"{message.content}"
        )


        elements.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )


        elements.append(
            Spacer(1,15)
        )


    document.build(
        elements
    )


    return filename
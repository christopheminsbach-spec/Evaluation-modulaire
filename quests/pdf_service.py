from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet



def create_chat_pdf(conversation):


    folder = Path("media/chat_pdf")

    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        folder /
        f"hyrule_chat_{conversation.id}.pdf"
    )


    doc = SimpleDocTemplate(
        str(filename)
    )


    styles = getSampleStyleSheet()


    content=[]


    content.append(
        Paragraph(
            "Chat d'Hyrule",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )



    for message in conversation.messages.all():


        text = (
            f"{message.role.upper()} : "
            f"{message.content}"
        )


        content.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )


        content.append(
            Spacer(1,12)
        )



    doc.build(content)


    return filename
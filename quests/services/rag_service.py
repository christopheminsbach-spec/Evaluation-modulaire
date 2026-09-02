import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


QUESTIONS_FILE = (
    BASE_DIR /
    "data" /
    "zelda_questions.json"
)


def load_zelda_database():

    if not QUESTIONS_FILE.exists():
        return []

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def search_zelda_context(question):

    database = load_zelda_database()

    question_lower = question.lower()


    results = []


    for item in database:

        text = (
            item["question"]
            .lower()
        )


        keywords = (
            question_lower
            .split()
        )


        score = 0


        for word in keywords:

            if word in text:

                score += 1



        if score > 0:

            results.append(
                {
                    "question":
                        item["question"],

                    "answer":
                        item.get(
                            "answer",
                            ""
                        ),

                    "category":
                        item["category"],

                    "score":
                        score
                }
            )



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return results[:5]



def build_context(question):


    results = search_zelda_context(
        question
    )


    if not results:

        return (
            "Aucune information "
            "spécifique trouvée."
        )



    context = ""


    for item in results:

        context += f"""

Question connue :
{item['question']}

Réponse :
{item['answer']}

Catégorie :
{item['category']}

---
"""


    return context
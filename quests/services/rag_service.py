import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_FILE = (
    BASE_DIR /
    "data" /
    "zelda_qa.json"
)



def load_zelda_memory():

    if not DATA_FILE.exists():

        return []


    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def build_context(question):

    knowledge = load_zelda_memory()


    results = []


    question_lower = (
        question.lower()
    )


    for item in knowledge:


        text = (
            item["question"]
            +
            " "
            +
            item["answer"]
        ).lower()


        words = question_lower.split()


        score = sum(
            1
            for word in words
            if word in text
        )


        if score > 0:

            results.append(
                (
                    score,
                    item
                )
            )


    results.sort(
        reverse=True,
        key=lambda x:x[0]
    )


    best_results = [
        item
        for score,item in results[:5]
    ]


    context = ""


    for item in best_results:

        context += f"""

Question :
{item['question']}

Réponse :
{item['answer']}

"""

    return context
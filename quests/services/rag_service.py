import json
from pathlib import Path
from difflib import SequenceMatcher


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_FILE = BASE_DIR / "data" / "zelda_knowledge.json"


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return []

    try:
        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("questions", [])

    except (
        OSError,
        json.JSONDecodeError
    ):
        return []

    return []


def similarity(text1, text2):
    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()


def search_knowledge(question, limit=3):

    knowledge = load_knowledge()

    if not knowledge:
        return []

    question = question.strip().lower()

    results = []

    for item in knowledge:

        question_text = str(
            item.get("question", "")
        )

        answer = str(
            item.get("answer", "")
        )

        category = str(
            item.get("category", "")
        )

        if not question_text or not answer:
            continue

        score = similarity(
            question,
            question_text
        )

        words = question.split()

        for word in words:

            if len(word) < 3:
                continue

            if word in question_text.lower():
                score += 0.08

            if word in answer.lower():
                score += 0.04

            if word in category.lower():
                score += 0.05

        results.append({
            "id": item.get("id"),
            "question": question_text,
            "answer": answer,
            "category": category,
            "score": score,
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]


def build_context(question, limit=3):

    results = search_knowledge(
        question,
        limit=limit
    )

    if not results:
        return ""

    context = []

    for item in results:

        context.append(
            f"""
Question de la base :
{item["question"]}

Réponse de la base :
{item["answer"]}

Catégorie :
{item["category"]}
""".strip()
        )

    return "\n\n---\n\n".join(context)
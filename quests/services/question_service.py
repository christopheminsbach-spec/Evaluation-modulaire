
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = BASE_DIR / "data" / "zelda_questions.json"


def get_questions():
    if not QUESTIONS_FILE.exists():
        return []

    try:
        with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
            questions = json.load(file)

    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(questions, list):
        return []

    return questions


def get_question(question_id):
    questions = get_questions()

    for question in questions:

        if question.get("id") == question_id:
            return question

    return None


def get_categories():
    questions = get_questions()

    categories = sorted({
        question.get("category")
        for question in questions
        if question.get("category")
    })

    return categories


def get_questions_by_category(category):
    questions = get_questions()

    return [
        question
        for question in questions
        if question.get("category", "").lower()
        == category.lower()
    ]


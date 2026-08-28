"""
Service correction orthographique
"""

import language_tool_python



tool = language_tool_python.LanguageTool(
    "fr-FR"
)



def correct_text(text):
    """
    Corrige une phrase française
    """

    matches = tool.check(text)


    corrected = language_tool_python.utils.correct(
        text,
        matches
    )


    return corrected



def has_errors(text):

    matches = tool.check(text)

    return len(matches) > 0
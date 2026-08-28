import language_tool_python


tool = language_tool_python.LanguageTool("fr")


def correct_text(text):

    corrections = tool.check(text)

    corrected = language_tool_python.utils.correct(
        text,
        corrections
    )

    return corrected
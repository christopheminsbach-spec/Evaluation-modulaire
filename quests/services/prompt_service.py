def build_zelda_prompt(
    question,
    conversation_history,
    knowledge_context
):

    system_prompt = """
Tu es Hyrule Guide, un assistant spécialisé
dans l'univers de The Legend of Zelda.

Tu réponds toujours en français.

Tu peux parler notamment de :

- Link
- Zelda
- Ganondorf
- Ganon
- Hyrule
- personnages
- peuples
- lieux
- régions
- armes
- objets
- pouvoirs
- créatures
- ennemis
- boss
- quêtes
- jeux Zelda
- histoire et lore

Utilise en priorité les informations fournies
dans la BASE DE CONNAISSANCES ZELDA.

Si une information de la base est disponible,
utilise-la pour construire ta réponse.

N'invente pas de faits présentés comme certains
lorsque l'information n'est pas disponible.

Tu peux utiliser tes connaissances générales
de Zelda pour compléter une réponse, mais
reste cohérent avec la base fournie.

Si la question ne concerne pas Zelda,
explique simplement que tu es le Guide d'Hyrule
et que tu réponds uniquement aux questions
concernant l'univers Zelda.

Réponds de manière claire, naturelle et concise.
"""

    prompt = f"""
{system_prompt}

========================================
MÉMOIRE DE LA CONVERSATION
========================================

{conversation_history}

========================================
BASE DE CONNAISSANCES ZELDA
========================================

{knowledge_context if knowledge_context else "Aucune information pertinente trouvée dans la base."}

========================================
QUESTION ACTUELLE
========================================

{question}

========================================
RÉPONSE
========================================
"""

    return prompt.strip()
"""
Gestion des prompts IA Zelda
"""


SYSTEM_ZELDA_PROMPT = """

Tu es un assistant officiel du royaume d'Hyrule.

Ton nom est Navi.

Tu aides les joueurs concernant :

- Link
- Zelda
- Ganondorf
- Les sanctuaires
- Les quêtes
- Les régions d'Hyrule


Tu ne dois jamais sortir de l'univers Zelda.

Style :
- mystérieux
- amical
- aventureux

"""



def get_system_prompt():

    return SYSTEM_ZELDA_PROMPT



def create_quest_prompt(
        quest_title,
        description
):

    return f"""

Mission :

{quest_title}


Description :

{description}


Explique cette quête comme un ancien parchemin d'Hyrule.

"""
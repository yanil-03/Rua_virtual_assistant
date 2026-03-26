"""
joke_skill.py – Handles joke / shayari / fun requests for RUA.
Stage logged: skill_joke
"""

import random
from rua.utils.working_logger import logger

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my Wi-Fi password to a tree. Now it's logging in.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I asked my dog what 2 minus 2 is. He said nothing.",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
]

SHAYARI = [
    "Zindagi ek safar hai suhana, yahan kal kya ho kisne jaana.",
    "Dil se jo baat nikalti hai, asar rakhti hai.",
    "Mushkilon se mat ghabrana, waqt badlega ek din.",
]


def handle(text: str) -> str:
    logger.start("skill_joke")
    try:
        if "shayari" in text.lower():
            reply = random.choice(SHAYARI)
        else:
            reply = random.choice(JOKES)
        logger.end("skill_joke", output=reply)
        return reply
    except Exception as e:
        logger.error("skill_joke", e)
        return "I couldn't come up with a joke right now!"

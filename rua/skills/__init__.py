"""
skills/__init__.py

Skills are modular handlers for specific intents.
Each skill exposes a `handle(text)` function.
"""

from rua.skills import time_skill, joke_skill, reminder_skill

SKILL_MAP = {
    "time":     time_skill.handle,
    "joke":     joke_skill.handle,
    "reminder": reminder_skill.handle,
}


def dispatch(intent: str, text: str) -> str | None:
    """
    Try to handle `intent` with a built-in skill.
    Returns None if no skill matches (fall through to LLM).
    """
    handler = SKILL_MAP.get(intent)
    if handler:
        return handler(text)
    return None

"""
router.py – Intent detection and LLM routing for RUA.

Stage logged: router

Determines what the user wants and which LLM backend to call.
"""

from rua.utils.working_logger import logger
from rua.utils.config import LLM_BACKEND

# ─── Keyword → Intent Map ─────────────────────────────────────────────────────
_INTENT_KEYWORDS = {
    "time":      ["time", "clock", "what time"],
    "weather":   ["weather", "temperature", "forecast", "rain", "sunny"],
    "reminder":  ["remind", "reminder", "alarm", "set alarm"],
    "music":     ["play", "music", "song", "spotify"],
    "joke":      ["joke", "funny", "laugh", "shayari"],
    "home":      ["light", "fan", "AC", "switch", "turn on", "turn off"],
    "whatsapp":  ["whatsapp", "message", "send message"],
    "mail":      ["email", "mail", "send mail"],
    "calendar":  ["calendar", "schedule", "meeting", "event"],
    "general":   [],   # fallback
}


def detect_intent(text: str) -> str:
    """Return the matched intent key or 'general'."""
    text_lower = text.lower()
    for intent, keywords in _INTENT_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return intent
    return "general"


# ─── Route ────────────────────────────────────────────────────────────────────

def route(text: str) -> str:
    """
    Detect intent, pick the right LLM backend, call it, and return the response.

    Returns the assistant's response string.
    """
    logger.start("router")

    intent = detect_intent(text)
    logger.info("router", f"Intent detected: '{intent}' | backend: '{LLM_BACKEND}'")

    # ── Try built-in skills first ─────────────────────────────────────────────
    try:
        from rua.skills import dispatch as skill_dispatch
        skill_response = skill_dispatch(intent, text)
        if skill_response is not None:
            logger.info("router", f"Handled by skill: '{intent}'")
            logger.end("router", output=intent)
            return skill_response
    except Exception as e:
        logger.error("router", e)

    # ── Fall back to LLM ──────────────────────────────────────────────────────
    try:
        if LLM_BACKEND == "cloud":
            from rua.brain.cloud_llm import generate as cloud_generate
            response = cloud_generate(text)
        else:
            from rua.brain.local_llm import generate as local_generate
            response = local_generate(text)

        logger.end("router", output=intent)
        return response

    except Exception as e:
        logger.error("router", e)
        return "Sorry, I ran into an issue processing your request."
"""
speaker.py – Text-to-Speech output for RUA.

Stages logged:
  - tts     : text → synthesised audio (pyttsx3)
  - speaker : playing the audio to the user
"""

import pyttsx3
from rua.utils.working_logger import logger
from rua.utils.config import TTS_RATE, TTS_VOLUME

# ─── Engine Initialisation ────────────────────────────────────────────────────

def _get_engine() -> pyttsx3.Engine:
    engine = pyttsx3.init()
    engine.setProperty("rate",   TTS_RATE)
    engine.setProperty("volume", TTS_VOLUME)
    return engine


# ─── speak() ──────────────────────────────────────────────────────────────────

def speak(text: str):
    """
    Convert `text` to speech and play it.

    Two logged stages:
      tts     – text is rendered to audio by the engine
      speaker – audio is sent to the audio device and played
    """
    if not text:
        logger.info("speaker", "speak() called with empty text – skipping")
        return

    # ── Stage: tts ────────────────────────────────────────────────────────────
    logger.start("tts")
    try:
        engine = _get_engine()
        logger.info("tts", f"Synthesising {len(text.split())} words")
        logger.end("tts", output="audio_ready")
    except Exception as e:
        logger.error("tts", e)
        return

    # ── Stage: speaker ────────────────────────────────────────────────────────
    logger.start("speaker")
    try:
        engine.say(text)
        engine.runAndWait()
        logger.end("speaker", output="played")
    except Exception as e:
        logger.error("speaker", e)
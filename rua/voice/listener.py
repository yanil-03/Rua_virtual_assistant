"""
listener.py – Microphone input handler for RUA.

Stages logged:
  - wake_word  : watching for "rua" (or configured WAKE_WORD)
  - listener   : recording & transcribing the user's actual command
"""

import speech_recognition as sr
from rua.utils.working_logger import logger
from rua.utils.config import (
    WAKE_WORD, SPEECH_LANG,
    LISTEN_TIMEOUT, PHRASE_LIMIT,
)

_recogniser = sr.Recognizer()


# ─── Internal: Transcribe One Audio Capture ───────────────────────────────────

def _transcribe(source: sr.Microphone, stage: str, timeout: int = None) -> str:
    """
    Listen on `source` and return the transcribed text.
    Returns "" on failure.
    """
    try:
        audio = _recogniser.listen(source, timeout=timeout, phrase_time_limit=PHRASE_LIMIT)
        text  = _recogniser.recognize_google(audio, language=SPEECH_LANG).lower().strip()
        return text
    except sr.WaitTimeoutError:
        logger.info(stage, "Timeout – no speech detected")
        return ""
    except sr.UnknownValueError:
        logger.info(stage, "Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(stage, e)
        return ""


# ─── Stage 1: Wake Word Detection ─────────────────────────────────────────────

def listen_for_wake_word() -> bool:
    """
    Block until the wake word is detected.
    Returns True when triggered, False on error.
    """
    logger.start("wake_word")
    logger.info("wake_word", f"Waiting for wake word: '{WAKE_WORD}'")

    try:
        with sr.Microphone() as source:
            _recogniser.adjust_for_ambient_noise(source, duration=0.5)

            while True:
                text = _transcribe(source, "wake_word", timeout=None)
                if WAKE_WORD in text:
                    logger.info("wake_word", f"Wake word detected in: '{text}'")
                    logger.end("wake_word", output=text)
                    return True

    except Exception as e:
        logger.error("wake_word", e)
        return False


# ─── Stage 2: Command Listener ────────────────────────────────────────────────

def listen() -> str:
    """
    Record and transcribe the user's command after wake word.
    Returns transcribed text or "" on failure.
    """
    logger.start("listener")
    logger.info("listener", "Listening for command…")

    try:
        with sr.Microphone() as source:
            _recogniser.adjust_for_ambient_noise(source, duration=0.3)
            text = _transcribe(source, "listener", timeout=LISTEN_TIMEOUT)

        logger.end("listener", output=text)
        return text

    except Exception as e:
        logger.error("listener", e)
        return ""
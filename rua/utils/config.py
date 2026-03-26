"""
config.py – Central configuration for RUA.

Edit the values here or override them via environment variables.
All other modules import from here, so one change propagates everywhere.
"""

import os

# ─── Wake Word ────────────────────────────────────────────────────────────────
WAKE_WORD = os.getenv("RUA_WAKE_WORD", "rua")   # the trigger phrase

# ─── LLM Backend ─────────────────────────────────────────────────────────────
# "local"  → Ollama (no internet needed)
# "cloud"  → Google Gemini (requires GEMINI_API_KEY env var)
LLM_BACKEND  = os.getenv("RUA_LLM_BACKEND", "local")   # "local" | "cloud"
LOCAL_MODEL  = os.getenv("RUA_LOCAL_MODEL",  "llama3")  # Ollama model name
CLOUD_MODEL  = os.getenv("RUA_CLOUD_MODEL",  "gemini-1.5-flash")
GEMINI_KEY   = os.getenv("GEMINI_API_KEY",   "")        # set in your env

# ─── Speech Recognition ───────────────────────────────────────────────────────
SPEECH_LANG     = os.getenv("RUA_SPEECH_LANG", "en-IN")   # auto language detect
LISTEN_TIMEOUT  = int(os.getenv("RUA_LISTEN_TIMEOUT", "5"))   # seconds to wait for speech
PHRASE_LIMIT    = int(os.getenv("RUA_PHRASE_LIMIT",   "10"))   # max recording seconds

# ─── TTS ──────────────────────────────────────────────────────────────────────
TTS_RATE   = int(os.getenv("RUA_TTS_RATE",   "175"))   # words per minute
TTS_VOLUME = float(os.getenv("RUA_TTS_VOL",  "1.0"))   # 0.0 – 1.0

# ─── Memory ───────────────────────────────────────────────────────────────────
MAX_MEMORY_TURNS = int(os.getenv("RUA_MEMORY_TURNS", "10"))   # keep last N turns

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "working_logs")
LOG_FILE = os.path.join(LOG_DIR, "working_logs.log")

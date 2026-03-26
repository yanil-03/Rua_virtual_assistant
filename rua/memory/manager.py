"""
manager.py – Short-term conversation memory for RUA.

Stage logged: memory

Stores the last MAX_MEMORY_TURNS turns (user + assistant messages) in memory.
Provides context strings for LLM prompts.
"""

from rua.utils.working_logger import logger
from rua.utils.config import MAX_MEMORY_TURNS


class MemoryManager:
    """
    Simple in-memory conversation history.

    Each turn is stored as:
        {"role": "user" | "assistant", "text": "..."}
    """

    def __init__(self):
        self._history: list[dict] = []

    # ──────────────────────────────────────────────────────────────────────────
    # Write
    # ──────────────────────────────────────────────────────────────────────────

    def add(self, role: str, text: str):
        """Append a message and trim to MAX_MEMORY_TURNS pairs."""
        logger.start("memory")

        entry = {"role": role, "text": text}
        self._history.append(entry)

        # Keep only the most recent N turns (each turn = 1 entry)
        if len(self._history) > MAX_MEMORY_TURNS * 2:
            self._history = self._history[-(MAX_MEMORY_TURNS * 2):]

        logger.info("memory", f"Stored {role} turn | history depth: {len(self._history)}")
        logger.end("memory", output=f"{len(self._history)} entries")

    # ──────────────────────────────────────────────────────────────────────────
    # Read
    # ──────────────────────────────────────────────────────────────────────────

    def get_history(self) -> list[dict]:
        """Return raw history list (for Gemini chat API)."""
        return list(self._history)

    def get_context_string(self) -> str:
        """
        Return history as a plain-text block for Ollama prompt injection.

        Example:
            User: hello rua
            Rua: Hello! How can I help?
        """
        lines = []
        for entry in self._history:
            speaker = "User" if entry["role"] == "user" else "Rua"
            lines.append(f"{speaker}: {entry['text']}")
        return "\n".join(lines)

    def clear(self):
        """Wipe conversation history (e.g., on new session)."""
        self._history.clear()
        logger.info("memory", "History cleared")


# ─── Global Singleton ─────────────────────────────────────────────────────────
memory = MemoryManager()

import os
import time
import json
import uuid
import traceback
from datetime import datetime

# ─── Log File Path ────────────────────────────────────────────────────────────
LOG_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "working_logs")
LOG_FILE = os.path.join(LOG_DIR, "working_logs.log")

os.makedirs(LOG_DIR, exist_ok=True)


class WorkingLogger:
    """
    Structured JSON logger for every RUA pipeline stage.

    Each conversation turn gets a unique request_id so you can
    trace an entire request across listener → router → llm → tts → speaker.

    Log format (one JSON line per event):
        {
            "time":        "2026-03-26 15:35:22.123456",
            "request_id":  "abc123-...",
            "stage":       "listener",
            "event":       "START | END | STREAM | INFO | ERROR | REQUEST_START | REQUEST_END",
            "latency_sec": 0.82,        # only on END
            "output":      "...",       # only on END
            "tokens":      120,         # only on LLM END
            "chunk":       "...",       # only on STREAM
            "message":     "...",       # only on INFO
            "error":       "...",       # only on ERROR
            "trace":       "..."        # only on ERROR
        }
    """

    def __init__(self):
        self.start_times: dict = {}
        self.request_id:  str  = None

    # ──────────────────────────────────────────────────────────────────────────
    # Request Lifecycle
    # ──────────────────────────────────────────────────────────────────────────

    def new_request(self) -> str:
        """Generate a new request_id and log REQUEST_START. Call once per turn."""
        self.request_id = str(uuid.uuid4())[:8]   # short 8-char ID for readability
        self.start_times.clear()                   # reset latency timers

        self._write({
            "time":       self._now(),
            "stage":      "request",
            "event":      "REQUEST_START",
            "request_id": self.request_id,
        })
        return self.request_id

    def end_request(self):
        """Log REQUEST_END at the close of a conversation turn."""
        self._write({
            "time":  self._now(),
            "stage": "request",
            "event": "REQUEST_END",
        })

    # ──────────────────────────────────────────────────────────────────────────
    # Core Writer
    # ──────────────────────────────────────────────────────────────────────────

    def _write(self, data: dict):
        """Attach request_id, serialise to JSON, append to log file + console."""
        data["request_id"] = self.request_id

        # Remove None values to keep logs clean
        clean = {k: v for k, v in data.items() if v is not None}
        line  = json.dumps(clean, ensure_ascii=False)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        print(f"[RUA LOG] {line}")

    @staticmethod
    def _now() -> str:
        return str(datetime.now())

    # ──────────────────────────────────────────────────────────────────────────
    # Stage Lifecycle  (START → END)
    # ──────────────────────────────────────────────────────────────────────────

    def start(self, stage: str):
        """Mark the beginning of a pipeline stage."""
        self.start_times[stage] = time.time()
        self._write({
            "time":  self._now(),
            "stage": stage,
            "event": "START",
        })

    def end(self, stage: str, output=None, tokens: int = None):
        """Mark the end of a pipeline stage with optional output and token count."""
        latency = round(time.time() - self.start_times.get(stage, time.time()), 3)
        self._write({
            "time":        self._now(),
            "stage":       stage,
            "event":       "END",
            "latency_sec": latency,
            "output":      output,
            "tokens":      tokens,
        })

    # ──────────────────────────────────────────────────────────────────────────
    # Streaming
    # ──────────────────────────────────────────────────────────────────────────

    def stream(self, stage: str, chunk: str):
        """Log an LLM streaming chunk."""
        self._write({
            "time":  self._now(),
            "stage": stage,
            "event": "STREAM",
            "chunk": chunk,
        })

    # ──────────────────────────────────────────────────────────────────────────
    # Info
    # ──────────────────────────────────────────────────────────────────────────

    def info(self, stage: str, message: str):
        """Log a free-form informational message for a stage."""
        self._write({
            "time":    self._now(),
            "stage":   stage,
            "event":   "INFO",
            "message": message,
        })

    # ──────────────────────────────────────────────────────────────────────────
    # Error Logging
    # ──────────────────────────────────────────────────────────────────────────

    def error(self, stage: str, err: Exception):
        """Log an exception with full traceback."""
        self._write({
            "time":  self._now(),
            "stage": stage,
            "event": "ERROR",
            "error": str(err),
            "trace": traceback.format_exc(),
        })


# ─── Global Singleton ─────────────────────────────────────────────────────────
logger = WorkingLogger()
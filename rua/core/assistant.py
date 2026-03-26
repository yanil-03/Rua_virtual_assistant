"""
assistant.py – Core orchestrator for RUA.

Full pipeline per turn:
  1. listen_for_wake_word()  →  wake_word stage
  2. listen()                →  listener stage
  3. memory.add(user, text)  →  memory stage
  4. route(text)             →  router stage → llm / cloud_llm stage
  5. memory.add(rua, resp)   →  memory stage
  6. speak(response)         →  tts + speaker stages

A new request_id is generated at the top of every turn via logger.new_request().
"""

from rua.utils.working_logger import logger
from rua.voice.listener        import listen_for_wake_word, listen
from rua.voice.speaker         import speak
from rua.brain.router          import route
from rua.memory.manager        import memory


def run():
    """
    Main assistant loop.
    Runs forever until interrupted (Ctrl+C).
    """
    print("\n🎙️  RUA is starting… say 'rua' to begin.\n")
    logger.info("assistant", "RUA started")

    try:
        while True:
            # ── Step 0: New request_id for this conversation turn ─────────────
            request_id = logger.new_request()
            print(f"\n── New Turn [{request_id}] ──────────────────────────────────")

            # ── Step 1: Wake word ─────────────────────────────────────────────
            triggered = listen_for_wake_word()
            if not triggered:
                logger.info("assistant", "Wake word not triggered, retrying…")
                logger.end_request()
                continue

            # ── Step 2: Listen for command ────────────────────────────────────
            text = listen()
            if not text:
                speak("I didn't catch that. Please try again.")
                logger.end_request()
                continue

            # ── Step 3: Store user turn in memory ─────────────────────────────
            memory.add("user", text)

            # ── Step 4: Route to LLM and get response ─────────────────────────
            response = route(text)

            # ── Step 5: Store assistant turn in memory ────────────────────────
            memory.add("assistant", response)

            # ── Step 6: Speak the response ────────────────────────────────────
            speak(response)

            # ── End of turn ───────────────────────────────────────────────────
            logger.end_request()

    except KeyboardInterrupt:
        print("\n\n👋 RUA shutting down. Goodbye!")
        logger.info("assistant", "Shutdown via KeyboardInterrupt")

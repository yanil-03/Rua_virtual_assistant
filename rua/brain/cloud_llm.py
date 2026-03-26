"""
cloud_llm.py – Google Gemini cloud LLM integration for RUA.

Stage logged: cloud_llm
  - Logs token usage from Gemini API response metadata
"""

import google.generativeai as genai
from rua.utils.working_logger import logger
from rua.utils.config import CLOUD_MODEL, GEMINI_KEY
from rua.memory.manager import memory


def _init_model():
    if not GEMINI_KEY:
        raise EnvironmentError("GEMINI_API_KEY is not set. Add it to your environment variables.")
    genai.configure(api_key=GEMINI_KEY)
    return genai.GenerativeModel(CLOUD_MODEL)


def generate(prompt: str) -> str:
    """
    Send `prompt` to Google Gemini and return the response text.
    Logs token usage from the API response metadata.
    """
    logger.start("cloud_llm")
    logger.info("cloud_llm", f"Model: {CLOUD_MODEL} | Prompt length: {len(prompt)} chars")

    try:
        model = _init_model()

        # Build context from memory
        history = memory.get_history()
        chat    = model.start_chat(history=[
            {"role": turn["role"], "parts": [turn["text"]]}
            for turn in history
        ])

        response = chat.send_message(prompt)

        # Extract token counts from Gemini metadata
        usage        = getattr(response, "usage_metadata", None)
        total_tokens = getattr(usage, "total_token_count", None) if usage else None
        input_tokens = getattr(usage, "prompt_token_count", None) if usage else None

        logger.info("cloud_llm", f"Input tokens: {input_tokens} | Total tokens: {total_tokens}")
        logger.end("cloud_llm", output=response.text.strip(), tokens=total_tokens)

        return response.text.strip()

    except EnvironmentError as e:
        logger.error("cloud_llm", e)
        return "Cloud LLM is not configured. Please set GEMINI_API_KEY."

    except Exception as e:
        logger.error("cloud_llm", e)
        return "Sorry, I couldn't reach the cloud right now."

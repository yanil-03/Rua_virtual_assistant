"""
local_llm.py – Ollama (local) LLM integration for RUA.

Stage logged: llm
  - Streams response chunks with logger.stream()
  - Logs final token count on END
"""

import requests
import json
from rua.utils.working_logger import logger
from rua.utils.config import LOCAL_MODEL
from rua.memory.manager import memory


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate(prompt: str) -> str:
    """
    Send `prompt` to the local Ollama model and return the full response.
    Streams each token chunk and logs them individually.
    """
    logger.start("llm")
    logger.info("llm", f"Model: {LOCAL_MODEL} | Prompt length: {len(prompt)} chars")

    # Build context from memory
    history = memory.get_context_string()
    full_prompt = f"{history}\nUser: {prompt}\nRua:" if history else f"User: {prompt}\nRua:"

    payload = {
        "model":  LOCAL_MODEL,
        "prompt": full_prompt,
        "stream": True,
    }

    response_text = ""
    token_count   = 0

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=30) as resp:
            resp.raise_for_status()

            for raw_line in resp.iter_lines():
                if not raw_line:
                    continue
                chunk_data = json.loads(raw_line)
                chunk      = chunk_data.get("response", "")

                if chunk:
                    logger.stream("llm", chunk)
                    response_text += chunk
                    token_count   += 1   # each streamed piece ≈ 1 token

                if chunk_data.get("done", False):
                    # Ollama may provide eval_count (actual tokens)
                    token_count = chunk_data.get("eval_count", token_count)
                    break

        logger.end("llm", output=response_text.strip(), tokens=token_count)
        return response_text.strip()

    except requests.exceptions.ConnectionError:
        err = ConnectionError("Ollama is not running. Start with: ollama serve")
        logger.error("llm", err)
        return "I couldn't reach my local brain. Is Ollama running?"

    except Exception as e:
        logger.error("llm", e)
        return "Something went wrong with the local model."
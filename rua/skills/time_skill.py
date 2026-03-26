"""
time_skill.py – Handles time queries for RUA.
Stage logged: skill_time
"""

from datetime import datetime
from rua.utils.working_logger import logger


def handle(text: str) -> str:
    logger.start("skill_time")
    try:
        now   = datetime.now()
        reply = f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d %Y')}."
        logger.end("skill_time", output=reply)
        return reply
    except Exception as e:
        logger.error("skill_time", e)
        return "I couldn't get the time right now."

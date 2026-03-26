"""
reminder_skill.py – Handles reminder / alarm requests for RUA.
Stage logged: skill_reminder

Basic in-memory reminder store. A background thread fires reminders.
"""

import threading
import time
import re
from datetime import datetime, timedelta
from rua.utils.working_logger import logger

_reminders: list[dict] = []   # {"message": str, "fire_at": datetime}


def _scheduler():
    """Background thread: check reminders every 10 seconds."""
    while True:
        now = datetime.now()
        for r in list(_reminders):
            if now >= r["fire_at"]:
                print(f"\n🔔 REMINDER: {r['message']}")
                logger.info("skill_reminder", f"Fired: {r['message']}")
                _reminders.remove(r)
        time.sleep(10)


# Start scheduler thread once
_t = threading.Thread(target=_scheduler, daemon=True)
_t.start()


def _parse_minutes(text: str) -> int:
    """Extract number of minutes from text like 'remind me in 5 minutes'."""
    match = re.search(r"(\d+)\s*minute", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d+)\s*hour", text, re.IGNORECASE)
    if match:
        return int(match.group(1)) * 60
    return 5   # default: 5 minutes


def handle(text: str) -> str:
    logger.start("skill_reminder")
    try:
        minutes  = _parse_minutes(text)
        fire_at  = datetime.now() + timedelta(minutes=minutes)
        message  = text  # use full text as reminder message
        _reminders.append({"message": message, "fire_at": fire_at})

        reply = f"Reminder set! I'll remind you in {minutes} minute(s) at {fire_at.strftime('%I:%M %p')}."
        logger.end("skill_reminder", output=reply)
        return reply
    except Exception as e:
        logger.error("skill_reminder", e)
        return "I couldn't set the reminder. Please try again."

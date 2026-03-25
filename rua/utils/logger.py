import time
import uuid
import json
from datetime import datetime

class RuaLogger:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.steps = []

    def log(self, step, message, data=None):
        timestamp = datetime.now().isoformat()

        log_entry = {
            "trace_id": self.trace_id,
            "timestamp": timestamp,
            "step": step,
            "message": message,
            "data": data
        }

        print(json.dumps(log_entry, indent=2))

        with open("rua.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def start_step(self, step_name):
        step = {
            "name": step_name,
            "start": time.time()
        }
        self.steps.append(step)
        self.log(step_name, "START")

    def end_step(self, step_name):
        for step in self.steps:
            if step["name"] == step_name and "end" not in step:
                step["end"] = time.time()
                latency = step["end"] - step["start"]

                self.log(step_name, "END", {
                    "latency_sec": round(latency, 3)
                })
                break

    def stream(self, word):
        log_entry = {
            "trace_id": self.trace_id,
            "type": "stream",
            "word": word,
            "timestamp": datetime.now().isoformat()
        }

        print(word, end=" ", flush=True)

        with open("rua.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def final(self):
        total_time = time.time() - self.start_time

        self.log("TOTAL", "Execution complete", {
            "total_latency_sec": round(total_time, 3)
        })
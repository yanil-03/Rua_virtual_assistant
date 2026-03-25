from rua.brain.local_llm import generate

def route(prompt):
    # simple routing logic
    if "open" in prompt or "play" in prompt:
        return "skill"
    else:
        return generate(prompt)
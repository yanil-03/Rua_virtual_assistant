import os

folders = [
    "rua",
    "rua/core",
    "rua/voice",
    "rua/brain",
    "rua/memory",
    "rua/skills",
    "rua/utils",
    "data",
    "models"
]

files = {
    "rua/main.py": "",
    "rua/core/assistant.py": "",
    "rua/voice/listener.py": "",
    "rua/voice/speaker.py": "",
    "rua/brain/router.py": "",
    "rua/brain/local_llm.py": "",
    "rua/brain/cloud_llm.py": "",
    "rua/memory/memory.py": "",
    "rua/skills/manager.py": "",
    "rua/utils/config.py": "",
    "rua/__init__.py": "",
    "rua/core/__init__.py": "",
    "rua/voice/__init__.py": "",
    "rua/brain/__init__.py": "",
    "rua/memory/__init__.py": "",
    "rua/skills/__init__.py": "",
    "rua/utils/__init__.py": "",
    ".env": "",
    "requirements.txt": "",
    "steps.txt": ""
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file, content in files.items():
    with open(file, "w") as f:
        f.write(content)

print("RUA project structure created 🚀")
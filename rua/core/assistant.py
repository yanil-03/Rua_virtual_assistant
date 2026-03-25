from rua.voice.listener import listen
from rua.voice.speaker import speak
from rua.brain.router import route

def run():
    speak("Hello, I am Rua. How can I help you?")

    while True:
        text = listen()
        print("User:", text)

        if not text:
            continue

        response = route(text)

        print("Rua:", response)
        speak(response)
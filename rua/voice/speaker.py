import asyncio
import edge_tts

async def speak_async(text):
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
    await communicate.save("voice.mp3")

def speak(text):
    asyncio.run(speak_async(text))
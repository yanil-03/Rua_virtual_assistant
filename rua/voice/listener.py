import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

model = Model("models/vosk")
rec = KaldiRecognizer(model, 16000)

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
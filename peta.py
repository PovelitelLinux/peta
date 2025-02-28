import os
import vosk
import pyaudio
import subprocess

model = vosk.Model("./vosk-model-small-ru-0.22")
rec = vosk.KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Слушаю...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = rec.Result()
        text = result.split('"')[3]
        if "петя" in text.lower():
            command = f'espeak-ng -v ru -p 1 "Чо надо {text}"'
            subprocess.run(command, shell=True)

    else:
        print(rec.PartialResult())
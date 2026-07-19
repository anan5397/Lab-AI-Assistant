import sounddevice as sd
import numpy as np
from openwakeword.model import Model

model = Model(inference_framework="onnx")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

print("Listening for wake words...")

def callback(indata, frames, time, status):
    audio = indata.flatten()

    predictions = model.predict(audio)

    for wakeword, score in predictions.items():
        if score > 0.5:
            wake = wakeword
            print(wake,score)

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    blocksize=CHUNK_SIZE,
    callback=callback
):
    input("Press Enter to stop...\n")
    
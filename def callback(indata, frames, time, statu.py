from openwakeword.model import Model
import sounddevice as sd
import numpy as np

model = Model(inference_framework="onnx")

def callback(indata, frames, time, status):
    audio = indata.flatten()

    prediction = model.predict(audio)

    print(prediction["hey_jarvis"])
    score = prediction["hey_jarvis"]
    if score > 1e-4:
        print("Wake word detected!")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="int16",
    blocksize=1280,
    callback=callback
):
    input("Listening...")
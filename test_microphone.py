import numpy as np

def callback(indata, frames, time, status):
    audio = indata.flatten()

    print("Max:", np.max(np.abs(audio)))
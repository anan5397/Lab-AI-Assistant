from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write 
import numpy as np


#Listening part 
fs = 16000
duration = 5  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
sd.play(myrecording)
# print(myrecording.shape)
# print("Recording finish")
#print(myrecording.max())     
write("First.wav",fs,myrecording)

#Let it print out all the words
model = WhisperModel("small.en")
segments, info = model.transcribe("First.wav") #segment contains the wording and info contains other information related. 
for segment in segments:
    print(segment.text)



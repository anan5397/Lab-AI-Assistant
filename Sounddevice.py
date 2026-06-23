import sounddevice as sd
from scipy.io.wavfile import write 
import numpy as np
#print(sd.query_devices()) #List out all the device related to sound
#print(sd.default.device) #Find the default device being used
#print(sd.query_devices(1))

fs = 16000
duration = 5  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
sd.play(myrecording)
print(myrecording.shape)
print("Recording finish")
print(myrecording.max())     
write("thank.wav",fs,myrecording)


import sounddevice as sd
import subprocess
from scipy.io.wavfile import write,read
PIPER_EXE = r"C:\Users\anan_ra\Desktop\piper\piper.exe"
MODEL1 = r"C:\Users\anan_ra\Desktop\piper\voices\en_US-lessac-medium.onnx"

def speak(text):
    subprocess.run(
        [PIPER_EXE, "-m", MODEL1, "-f", "output.wav"], #Save the output as output.wav
        input=text,
        text=True
        )
    sample_rate, audio_data = read("output.wav")

    sd.play(audio_data, sample_rate)
    sd.wait()

speak("Hello, I am your AI Lab Assistant. How can I help you today?")
sample_rate, audio_data = read("output.wav")

print("Sample rate:", sample_rate)
print("Shape:", audio_data.shape)
print("Dtype:", audio_data.dtype)

sd.play(audio_data, sample_rate)
sd.wait()
import winsound

winsound.PlaySound("output.wav", winsound.SND_FILENAME)
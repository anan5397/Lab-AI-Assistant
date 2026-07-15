from openai import OpenAI
from dotenv import load_dotenv
import os
from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write,read
import numpy as np
from openwakeword.model import Model
import wakeword


model = Model(inference_framework="onnx")

#FOr checking env and API keys
#.venv\Scripts\activate for activating the environment
load_dotenv(override=True)
#Initialize the piper 
import subprocess

PIPER_EXE = r"C:\Users\anan_ra\Desktop\piper\piper.exe"
MODEL1 = r"C:\Users\anan_ra\Desktop\piper\voices\en_US-lessac-medium.onnx"


AI_state = "waiting for wake word"
def speak(text):
    subprocess.run(
        [PIPER_EXE, "-m", MODEL1, "-f", "output.wav"], #Save the output as output.wav
        input=text,
        text=True
        )
    sample_rate, audio_data = read("output.wav")

    sd.play(audio_data, sample_rate)
    sd.wait()

client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

model_whisper = WhisperModel("small.en")

audio_buffer = []
print("Jarvis is sleeping")
AI_state = "waiting_for_wake_word"

def callback(indata, frames, time, status): #This goes on in the background and keeps listening for the wake word.
    global AI_state
    global audio_buffer #This is a list that stores the audio data that is being recorded. It is used to store the audio data that is being recorded while the AI is listening for the wake word.
    global silent_chunk #This helps to keep track of the number of consecutive silent chunks. It is used to determine when the user has finished speaking.
    global heard_speech #This is a boolean variable that keeps track of whether the user has spoken or not. It is used to determine when the user has finished speaking.
    global conversation_end #This is a list that stores the conversation between the user and the AI. It is used to keep track of the conversation history.
    audio = indata.flatten() #Give us chunks of audio data in the form of a 1D array. A chunk is a small segment of audio data that is processed at a time.
    #print("Audio is now: ",audio[1])
    if AI_state == "waiting_for_wake_word":
        predictions = model.predict(audio)
        for wakeword, score in predictions.items():
            if score > 0.5:
                print("AI heard the wake word:",wakeword)
                print(wakeword, score)
                print("Listening...")
                AI_state = "listening"
                audio_buffer = []
                silent_chunk = 0
                heard_speech = False
                break

    elif AI_state == "listening":
         #Combines all chunks of audio data into a single array.
        loudness = np.average(np.abs(audio))
        # print("Loudness:", loudness)
        if  loudness < 50:
            silent_chunk += 1
        else:
            silent_chunk = 0
            heard_speech = True

        if silent_chunk >= 13 and heard_speech == True: #If there are 13 consecutive silent chunks, we assume the user has finished speaking.
            AI_state = "processing"
            print("Processing audio...")
            silent_chunk = 0
            heard_speech = False
        audio_buffer.extend(audio)
    
    elif AI_state == "speaking":
        pass


conversation = [
    {
        "role": "system",
        "content": "You are a laboratory safety assistant."
    }
]

import time
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="int16",
    blocksize=1280,
    callback=callback
):
    while True:
        time.sleep(0.1)  # Sleep for a short duration to reduce CPU usage

    

        if AI_state == "processing": #Processing the audio and sending it to GPT.
            print("Processing audio...")
            audio_np = np.array(audio_buffer, dtype=np.int16)
            write("command.wav", 16000, audio_np)#convert the audio buffer to a WAV file
            segments, info = model_whisper.transcribe("command.wav") #extracting the text from the audio file using whisper model.
            
            question = ""
            for segment in segments:
                print(segment.text)
                question += segment.text + " "
                conversation_end = False
                if "goodbye" in question.lower() or "thank you" in question.lower():
                    AI_state = "waiting_for_wake_word"
                    audio_buffer = []
                    print("AI is waiting for wake word...")
                    conversation_end = True
            with open("cleapss.txt", "r") as file:
               cleapss_data = file.read()

            print("Sending to GPT...")
            
            # Find relevant lines
            relevant_lines = []

  

            for line in cleapss_data.splitlines():

                # Split question into words
                question_words = question.lower().split()

                for word in question_words:

                    # Check if word exists in line
                    if word in line.lower():
                        relevant_lines.append(line)
                        break

            # Join relevant results
            context = "\n".join(relevant_lines)

            prompt = f"""
            Give only the final answer in one sentence.

            Do not explain the steps unless asked.

            Use plain text only.

            Safety Information:
            {context}

            Question:
            {question}
            """
            conversation.append(
             {
                  "role": "user",
                  "content": prompt
             }
                )
            # Send to ChatGPT
            global response
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=conversation
            ) 
            conversation.append(
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                }
            )
            #Send questions to CHATGPT as a user. 
            if conversation_end == True:
                speak("Goodbye")
                AI_state = "waiting_for_wake_word"
                audio_buffer = []
                print("AI is waiting for wake word...")
                conversation_end = False
            else:
                AI_state = "speaking"



        elif AI_state == "speaking" and conversation_end == False: #This is where the AI speaks the response from GPT.


            print("\nAI Lab Assistant:")
            reply = response.choices[0].message.content #This is actual response from AI. 
            clean_reply = reply.replace("*", "")
            print(clean_reply)
            speak(clean_reply) #This converts clean_reply to output.wav which gets updated after every questions
            sample_rate, audio_data = read("output.wav") #Extracting the file
            # sd.play(audio_data, sample_rate)
            # sd.wait()
            audio_buffer = []
            AI_state = "listening"
            


















































































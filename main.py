from openai import OpenAI
from dotenv import load_dotenv
import os
from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write,read
import numpy as np
from openwakeword.model import Model
model = Model(inference_framework="onnx")

#FOr checking env and API keys
#.venv\Scripts\activate for activating the environment
load_dotenv(override=True)
#Initialize the piper 
import subprocess

PIPER_EXE = r"C:\Users\anan_ra\Desktop\piper\piper.exe"
MODEL = r"C:\Users\anan_ra\Desktop\piper\voices\en_US-lessac-medium.onnx"

def speak(text):
    subprocess.run(
        [PIPER_EXE, "-m", MODEL, "-f", "output.wav"], #Save the output as output.wav
        input=text,
        text=True
        )

client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

model_whisper = WhisperModel("small.en")

assistant_awake = False
def callback(indata, frames, time, status):
        global assistant_awake
        audio = indata.flatten()

        predictions = model.predict(audio)
        print(predictions)
        for wakeword, score in predictions.items():
             if score > 0.5:
                print("AI IS AWAKE")
                assistant_awake = True

import time
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    blocksize=CHUNK_SIZE,
    callback=callback
    ):
        while True:
              if assistant_awake:
                    assistant_awake = False  # reset trigger

                    print("Starting assistant...")
              time.sleep(0.5)
    
    

    
  

    # #Listening part 
    # fs = 16000
    # duration = 5  # seconds
    # print("Start speaking")
    # myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    # sd.wait()
    # write("First.wav",fs,myrecording)

    # #Let it print out all the words
    # segments, info = model_whisper.transcribe("First.wav") #segment contains the wording and info contains other information related. 
    # for segment in segments:
    #     print(segment.text)


    # question = segment.text
    # if "goodbye" in question.lower() or "thank you" in question.lower():
    #     speak("Goodbye")
    #     assistant_running = False
        

   

    # # Load local CLEAPSS data
    # with open("cleapss.txt", "r") as file:
    #     cleapss_data = file.read()

    # print("Sending to GPT...")
            
    # # Find relevant lines
    # relevant_lines = []

    # for line in cleapss_data.splitlines():

    #     # Split question into words
    #     question_words = question.lower().split()

    #     for word in question_words:

    #         # Check if word exists in line
    #         if word in line.lower():
    #             relevant_lines.append(line)
    #             break

    # # Join relevant results
    # context = "\n".join(relevant_lines)

    # prompt = f"""
    # Give only the final answer in one sentence.

    # Do not explain the steps unless asked.

    # Use plain text only.

    # Safety Information:
    # {context}

    # Question:
    # {question}
    # """

    # # Send to ChatGPT
    # response = client.chat.completions.create(
    #     model="gpt-4.1-mini",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # ) #Send questions to CHATGPT as a user. 

    # # Print result
    # print("\nAI Lab Assistant:")
    # reply = response.choices[0].message.content #This is actual response from AI. 
    # clean_reply = reply.replace("*", "")
    # print(clean_reply)
    # print("Assistant:", str(clean_reply))
    # speak(clean_reply) #This converts clean_reply to output.wav which gets updated after every questions
    # sample_rate, audio_data = read("output.wav") #Extracting the file
    # sd.play(audio_data, sample_rate)
    # sd.wait()





















































































#This code is everything but without the wake word
# #FOr checking env and API keys
# #.venv\Scripts\activate for activating the environment
# load_dotenv(override=True)
# #Initialize the piper 
# import subprocess

# PIPER_EXE = r"C:\Users\anan_ra\Desktop\piper\piper.exe"
# MODEL = r"C:\Users\anan_ra\Desktop\piper\voices\en_US-lessac-medium.onnx"

# def speak(text):
#     subprocess.run(
#         [PIPER_EXE, "-m", MODEL, "-f", "output.wav"], #Save the output as output.wav
#         input=text,
#         text=True
#         )


# client = OpenAI(
#         api_key=os.getenv("OPENAI_API_KEY")
#     )

# model = WhisperModel("small.en")

# assistant_running = True

# while assistant_running:

#     #Listening part 
#     fs = 16000
#     duration = 5  # seconds
#     print("Start speaking")
#     myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
#     sd.wait()
#     write("First.wav",fs,myrecording)

#     #Let it print out all the words
#     segments, info = model.transcribe("First.wav") #segment contains the wording and info contains other information related. 
#     for segment in segments:
#         print(segment.text)


#     question = segment.text
#     if "goodbye" in question.lower() or "thank you" in question.lower():
#         speak("Goodbye")
#         assistant_running = False
        

   

#     # Load local CLEAPSS data
#     with open("cleapss.txt", "r") as file:
#         cleapss_data = file.read()

#     print("Sending to GPT...")
            
#     # Find relevant lines
#     relevant_lines = []

#     for line in cleapss_data.splitlines():

#         # Split question into words
#         question_words = question.lower().split()

#         for word in question_words:

#             # Check if word exists in line
#             if word in line.lower():
#                 relevant_lines.append(line)
#                 break

#     # Join relevant results
#     context = "\n".join(relevant_lines)

#     prompt = f"""
#     Give only the final answer in one sentence.

#     Do not explain the steps unless asked.

#     Use plain text only.

#     Safety Information:
#     {context}

#     Question:
#     {question}
#     """

#     # Send to ChatGPT
#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     ) #Send questions to CHATGPT as a user. 

#     # Print result
#     print("\nAI Lab Assistant:")
#     reply = response.choices[0].message.content #This is actual response from AI. 
#     clean_reply = reply.replace("*", "")
#     print(clean_reply)
#     print("Assistant:", str(clean_reply))
#     speak(clean_reply) #This converts clean_reply to output.wav which gets updated after every questions
#     sample_rate, audio_data = read("output.wav") #Extracting the file
#     sd.play(audio_data, sample_rate)
#     sd.wait()






































































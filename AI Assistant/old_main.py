from openai import OpenAI
from dotenv import load_dotenv
import os
import pyttsx3 
engine = pyttsx3.init()
load_dotenv(override=True)
import speech_recognition as sr
#.venv\Scripts\activate for activating the environment
recognizer = sr.Recognizer()
#print(os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load local CLEAPSS data
with open("cleapss.txt", "r") as file:
    cleapss_data = file.read()


WAKE_WORD = "hey jarvis"

while True:

    with sr.Microphone() as source:

        print("Listening for wake word...")

        try:
            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=5
            )

            text = recognizer.recognize_google(audio).lower()

            print("Heard:", text)

            if WAKE_WORD in text:

                print("Wake word detected!")

                engine.say("Hello there, how can I help?")
                engine.runAndWait()

                # Listen for actual question
                print("Listening for question...")

                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=15
                )

                question = recognizer.recognize_google(audio)

                print("Question:", question)

                break

        except Exception as e:
            print(e)

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

# Send to ChatGPT
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
) #Send questions to CHATGPT as a user. 

# Print result
print("\nAI Lab Assistant:")
reply = response.choices[0].message.content
clean_reply = reply.replace("*", "")

print("Creating new TTS engine...")

engine.stop()
engine = pyttsx3.init()
print("Question:", question)
print("GPT reply:", reply)
print("About to speak...")

engine.say(clean_reply)
engine.runAndWait()

print("Finished speaking")
print("Speaking response...")
engine.say("testing one two three")
# engine.say(clean_reply)
engine.runAndWait()

print("Finished speaking")
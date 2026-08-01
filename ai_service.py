from openai import OpenAI
from dotenv import load_dotenv
import os

from rag import retrieve_context

load_dotenv()
load_dotenv(override=True)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("KEY:", os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str):

    print("Searching CLEAPSS database...")

    context = retrieve_context(question)

    if context == "":
        context = "No relevant CLEAPSS information found."


    messages = [
        {
            "role": "system",
            "content": """
            You are a laboratory safety assistant.

            Answer questions using CLEAPSS safety information.
            If information is unavailable, say you do not know.

            Give concise answers.
            Include safety warnings when relevant.
            """
        },
        {
            "role": "user",
            "content": f"""
            CLEAPSS Safety Information:

            {context}


            Question:

            {question}
            """
        }
    ]


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )


    return response.choices[0].message.content


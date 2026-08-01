from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import generate_answer


app = FastAPI() #Setting up the FastAPI application instance


class Question(BaseModel): #Making sure the input is a string
    question: str


@app.get("/") #Crerating a home route to check if the API is running
def home():
    return {
        "message": "Lab AI Assistant is running"
    }


@app.post("/ask") #Send requests to this endpoint to get answers from the AI assistant
def ask(data: Question):

    answer = generate_answer(data.question) #data.question is the question sent in the request body, which is passed to the generate_answer function to get an answer from the AI assistant

    return {
        "answer": answer
    }
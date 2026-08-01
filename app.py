from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import generate_answer


app = FastAPI()


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Lab AI Assistant is running"
    }


@app.post("/ask")
def ask(data: Question):

    answer = generate_answer(data.question)

    return {
        "answer": answer
    }
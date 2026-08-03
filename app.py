from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai_service import generate_answer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI() #Setting up the FastAPI application instance
templates = Jinja2Templates(directory="templates") #This is where the HTML templates are stored. The directory is set to "templates" which is where the HTML files are located.
app.mount("/static", StaticFiles(directory="static"), name="static")

class Question(BaseModel): #Making sure the input is a string
    question: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    ) #This is the home page of the application. It returns the index.html template when a GET request is made to the root URL ("/"). The request object is passed to the template for rendering.

@app.post("/ask") #Send requests to this endpoint to get answers from the AI assistant
def ask(data: Question):

    answer = generate_answer(data.question) #data.question is the question sent in the request body, which is passed to the generate_answer function to get an answer from the AI assistant

    return {
        "answer": answer
    }
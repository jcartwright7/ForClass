import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")

app = FastAPI(title="AI Study Buddy")
app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI(api_key=API_KEY) if API_KEY else None

class Question(BaseModel):
    text: str

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/ask")
def ask_ai(question: Question):
    if not question.text.strip():
        raise HTTPException(status_code=400, detail="Please enter a question.")

    if client is None or not MODEL:
        raise HTTPException(
            status_code=500,
            detail="AI service is not configured. Add the required environment variables."
        )

    try:
        response = client.responses.create(
            model=MODEL,
            input=(
                "You are a friendly study assistant. "
                "Explain ideas clearly for a school student. "
                "Do not invent facts. "
                "If you are unsure, say so.\n\n"
                f"Student question: {question.text}"
            )
        )
        return {"answer": response.output_text}

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {error}"
        )

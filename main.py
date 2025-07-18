from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/analyze-form")
async def analyze_form(fields: list):
    # fields = [{"name": "...", "label": "...", ...}, ...]
    # ここでGeminiに問い合わせて「どこに何を入れるか」を判定
    # サンプル応答
    return {"name": "input_1", "email": "input_2", ...}

@app.get("/")
async def root():
    return {"status": "ok"}


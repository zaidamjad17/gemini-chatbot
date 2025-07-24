from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
print("🔑 API KEY:", os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Read the Gemini API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Define the request body format
class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_with_gemini(data: Prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {"text": data.prompt}
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)

    if response.status_code == 200:
        content = response.json()
        try:
            return {"reply": content["candidates"][0]["content"]["parts"][0]["text"]}
        except Exception:
            return {"error": "Couldn't parse Gemini response."}
    else:
        return {"error": f"Gemini API failed with status code {response.status_code}", "details": response.text}

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# এনভায়রনমেন্ট ভেরিয়েবল থেকে API Key নেওয়া হচ্ছে
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# আধুনিক জেমিনি ফ্ল্যাশ মডেল সেটআপ
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Model initialization error: {e}")

class QueryModel(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "AERO AI Backend is Online!"}

@app.post("/chat")
def chat_with_ai(data: QueryModel):
    try:
        print(f"Received query: {data.query}")
        response = model.generate_content(data.query)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"সার্ভার ত্রুটি: {str(e)}"}

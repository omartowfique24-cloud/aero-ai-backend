from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# এনভায়রনমেন্ট ভেরিয়েবল থেকে API Key নেওয়া হচ্ছে (নিরাপত্তার জন্য)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

class QueryModel(BaseModel):
    query: str

@app.post("/chat")
def chat_with_ai(data: QueryModel):
    try:
        print(f"Received query: {data.query}") 
        response = model.generate_content(data.query)
        
        if response.text:
            return {"response": response.text}
        else:
            return {"response": "দুঃখিত, কোনো উত্তর পাওয়া যায়নি বা কনটেন্ট ব্লক করা হয়েছে।"}
            
    except Exception as e:
        print(f"Error: {str(e)}")
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            res = fallback_model.generate_content(data.query)
            return {"response": res.text}
        except Exception as err:
            return {"response": f"ত্রুটি হয়েছে: {str(err)}"}

@app.get("/")
def home():
    return {"message": "AERO AI Backend is Online!"}

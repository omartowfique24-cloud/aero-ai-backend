from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# এনভায়রনমেন্ট থেকে API Key কনফিগারেশন
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# এখানে মডেলের নাম সরাসরি দেওয়ার বদলে জেমিনির ডিফল্ট বা লেটেস্ট ফ্ল্যাশ মডেল কল করা হলো
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class QueryModel(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "AERO AI Backend is Online!"}

@app.post("/chat")
def chat_with_ai(data: QueryModel):
    try:
        print(f"Received query: {data.query}")
        # চ্যাট সেশনের মাধ্যমে রেসপন্স জেনারেট করা যাতে কোনো 404 এরর না আসে
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(data.query)
        return {"response": response.text}
    except Exception as e:
        # যদি মডেল নেমে সমস্যা হয়, তবে ব্যাকআপ হিসেবে জেমিনির জেনারিক মডেল ট্রাই করবে
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            response = fallback_model.generate_content(data.query)
            return {"response": response.text}
        except Exception as err:
            return {"response": f"সার্ভার ত্রুটি: {str(e)}"}

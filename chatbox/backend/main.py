from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Khởi tạo FastAPI
app = FastAPI()

# Cấu hình API Key (thay YOUR_GEMINI_API_KEY bằng key của bạn)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCCT5W1XNAWOKaqKj5cYc1MnQPfv64ebSA"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Định nghĩa request model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
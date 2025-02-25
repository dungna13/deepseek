from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import google.generativeai as genai
import os
import base64

# Khởi tạo FastAPI
app = FastAPI()

# Cấu hình API Key (thay YOUR_GEMINI_API_KEY bằng key của bạn)
os.environ["GOOGLE_API_KEY"] = "Your_API"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

@app.post("/chat/")
async def chat(
    message: str = Form(""),  # Nhận text
    image: UploadFile = File(None)  # Nhận file ảnh (tùy chọn)
):
    try:
        model = genai.GenerativeModel("gemini-pro-vision")

        # Xử lý input
        input_data = []
        if message:
            input_data.append(message)
        if image:
            image_data = {
                "mime_type": image.content_type,
                "data": encode_image(image.file),
            }
            input_data.append(image_data)

        # Gửi yêu cầu đến Gemini
        response = model.generate_content(input_data)

        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

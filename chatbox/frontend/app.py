import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat/"

st.title("💬 Chat với Gemini AI (Text & Image)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Hiển thị lịch sử chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Nhập text và ảnh
user_input = st.chat_input("Nhập tin nhắn của bạn...")
uploaded_file = st.file_uploader("Tải lên hình ảnh", type=["png", "jpg", "jpeg"])

if user_input or uploaded_file:
    st.session_state["messages"].append({"role": "user", "content": user_input or "🖼️ (Hình ảnh)"})

    with st.chat_message("user"):
        st.markdown(user_input or "🖼️ (Hình ảnh)")

    # Chuẩn bị payload
    files = {"image": uploaded_file} if uploaded_file else {}
    data = {"message": user_input} if user_input else {}

    # Gửi yêu cầu đến API
    response = requests.post(API_URL, data=data, files=files)
    bot_response = response.json().get("response", "Lỗi kết nối!")

    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

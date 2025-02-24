import streamlit as st
import requests

# URL của FastAPI backend
API_URL = "http://127.0.0.1:8000/chat/"

st.title("💬 Chat với Gemini AI")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Hiển thị lịch sử chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập nội dung chat
user_input = st.chat_input("Nhập tin nhắn của bạn...")

if user_input:
    # Hiển thị tin nhắn người dùng
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gửi yêu cầu đến FastAPI
    response = requests.post(API_URL, json={"message": user_input})
    bot_response = response.json().get("response", "Lỗi kết nối!")

    # Hiển thị phản hồi từ AI
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

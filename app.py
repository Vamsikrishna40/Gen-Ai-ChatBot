
import streamlit as st
from gemini_client import GeminiCareerChatbot

st.set_page_config(
    page_title="Career Advisor Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Career Advisor Chatbot")
st.write("Ask questions about career paths, skills, resumes, interviews, and learning roadmaps.")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = GeminiCareerChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("About")
    st.write("""
    This chatbot uses Google Gemini GenAI API to provide career guidance.
    
    You can ask about:
    - Career roadmaps
    - Resume tips
    - Interview preparation
    - Skill suggestions
    - Project ideas
    """)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chatbot = GeminiCareerChatbot()
        st.success("Chat history cleared.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask your career question...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_response = st.session_state.chatbot.get_response(user_input)
            st.markdown(bot_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })

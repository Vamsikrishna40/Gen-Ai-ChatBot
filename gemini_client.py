import os
import logging
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from prompts import CAREER_ADVISOR_PROMPT


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    filename=BASE_DIR / "chatbot_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class GeminiCareerChatbot:
    def __init__(self):
        api_key = None

        # First try Streamlit Cloud secrets
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

        # Then try local .env file
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Add it in Streamlit Cloud Secrets or local .env file."
            )

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=CAREER_ADVISOR_PROMPT
        )

        self.chat = self.model.start_chat(history=[])

    def get_response(self, user_message):
        try:
            if not user_message or user_message.strip() == "":
                return "Please enter a valid career-related question."

            response = self.chat.send_message(user_message)

            if response and response.text:
                return response.text

            return "I could not generate a response. Please try again."

        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return f"Error: {str(e)}"

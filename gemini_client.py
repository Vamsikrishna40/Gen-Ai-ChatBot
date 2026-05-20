
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import CAREER_ADVISOR_PROMPT

load_dotenv()

logging.basicConfig(
    filename="chatbot_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GeminiCareerChatbot:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
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
            else:
                return "I could not generate a response. Please try again."

        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return "Sorry, something went wrong while contacting the AI model. Please try again later."

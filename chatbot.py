import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

from utils.constants import MODEL_NAME
from prompt import PROMPTS

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """Initializes or switches the Gemini conversational context based on current app state."""
    if "genai_client" not in st.session_state:
        st.session_state.genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    current_page = st.session_state.get("current_page", "Dashboard Home")
    
    if "chat_session" not in st.session_state or force_rebuild:
        college_context = ""
        try:
            with open("data/college_info.txt", "r", encoding="utf-8") as f:
                college_context = f.read()
        except FileNotFoundError:
            pass
        
        base_instruction = PROMPTS.get(current_page, "You are a helpful assistant.")
        full_instruction = f"{base_instruction}\n\n[General Knowledge Context]:\n{college_context}"
        
        if current_page == "PDF Chat" and custom_pdf_text:
            full_instruction = f"{PROMPTS.get('PDF Chat', '')}\n\n[UPLOADED DOCUMENT CONTENT]:\n{custom_pdf_text}"
            
        st.session_state.chat_session = st.session_state.genai_client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=full_instruction,
                temperature=0.7,
            )
        )

def get_ai_stream_response(user_question: str):
    """Yields streaming chunks of text from the active conversation thread."""
    init_chatbot()
    try:
        # Calls the streaming endpoint of the new google-genai SDK
        response_stream = st.session_state.chat_session.send_message_stream(user_question)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"CampusAI Engine Error: {str(e)}"
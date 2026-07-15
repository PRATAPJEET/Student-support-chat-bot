import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load local environment variables if present (for local desktop running)
load_dotenv()

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """
    Initializes the Gemini API client.
    Checks Streamlit cloud secrets first, then falls back to local environment variables.
    """
    # 1. Try fetching from Streamlit Cloud Secrets vault
    # 2. Fall back to local .env configuration environment variable
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # Catch missing keys gracefully before the genai library throws an error
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets (Cloud) or .env file (Local).")
        st.stop()
        
    # Initialize the correct Google GenAI SDK Client
    if "genai_client" not in st.session_state:
        st.session_state.genai_client = genai.Client(api_key=api_key)

def get_ai_stream_response(messages):
    """
    Sends the message history to the Gemini API and returns the response string.
    Matches the exact import expected by app.py.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages
        )
        return response.text
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return "Sorry, I encountered an issue reaching out to the AI brain right now."
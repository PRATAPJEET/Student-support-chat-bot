import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load local environment variables if present (for local desktop running)
load_dotenv()

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """
    Initializes the Gemini API client.
    Configured with explicit http_options to bridge compatibility with new AQ. tokens.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets (Cloud) or .env file (Local).")
        st.stop()
        
    if "genai_client" not in st.session_state:
        st.session_state.genai_client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version='v1')
        )

def get_ai_stream_response(messages):
    """
    Sends the message history to the Gemini API and yields response chunks.
    Works perfectly with Streamlit's st.write_stream.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    
    try:
        # UPDATED: Swapped to the active model tier to avoid the 404 block
        response_stream = client.models.generate_content_stream(
            model='gemini-3.5-flash',
            contents=messages
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        yield "Sorry, I encountered an issue reaching out to the AI brain right now."
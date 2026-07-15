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
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets (Cloud) or .env file (Local).")
        st.stop()
        
    if "genai_client" not in st.session_state:
        st.session_state.genai_client = genai.Client(api_key=api_key)

def get_ai_stream_response(messages):
    """
    Sends the message history to the Gemini API and yields response chunks.
    Works perfectly with Streamlit's st.write_stream.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    
    try:
        # Notice we use generate_content_stream here instead of generate_content
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=messages
        )
        
        # Yield each text chunk as it arrives from the API
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        yield "Sorry, I encountered an issue reaching out to the AI brain right now."
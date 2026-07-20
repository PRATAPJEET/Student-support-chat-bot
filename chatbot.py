import streamlit as st
from google import genai
import google.genai.errors as errors
from dotenv import load_dotenv
import os

# Load API environment variables from the local .env configuration
load_dotenv()

def init_chatbot():
    """Initializes the Gemini API client interface using the saved environment keys."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing! Please check that GEMINI_API_KEY is configured in your parameters.")
        return None
    return genai.Client(api_key=api_key)

def get_ai_stream_response(client, prompt_history, user_message):
    """
    Sends conversational context to the Gemini engine and handles streaming text feedback.
    Gracefully catches 503 structural server spikes without breaking the dashboard UI.
    """
    if client is None:
        return
    
    try:
        # Build the live tracking context array out of the active user session history
        # (Replace 'gemini-2.5-flash' with the specific target model name your project runs)
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt_history + [{"role": "user", "parts": [user_message]}]
        )
        
        for chunk in response_stream:
            yield chunk.text
            
    except errors.APIError as e:
        if e.code == 503:
            st.error("⚠️ The AI server is experiencing heavy traffic spikes right now. Please wait a moment and resend your prompt!")
        else:
            st.error(f"An unexpected API connection error occurred: {e.message}")
    except Exception as e:
        st.error(f"System tracking error: {str(e)}")
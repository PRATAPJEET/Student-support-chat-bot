import streamlit as st
from google import genai
from google.genai import types
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
    Converts standard input history arrays into strict google.genai types.Content schemas.
    """
    if client is None:
        return
    
    try:
        # 1. Transform raw lists into strict Pydantic types.Content objects
        formatted_contents = []
        for message in prompt_history:
            role = message["role"]
            # Extract content string safely
            content_text = message["parts"][0] if isinstance(message["parts"], list) else message["parts"]
            
            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=content_text)]
                )
            )
        
        # 2. Append the latest live query to the target contents list
        formatted_contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            )
        )
        
        # 3. Call generate_content_stream with strict type arrays
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=formatted_contents
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
            
    except errors.APIError as e:
        if e.code == 503:
            st.error("⚠️ The AI server is experiencing heavy traffic spikes right now. Please wait a moment and resend your prompt!")
        else:
            st.error(f"An unexpected API connection error occurred: {e.message}")
    except Exception as e:
        st.error(f"System tracking error: {str(e)}")
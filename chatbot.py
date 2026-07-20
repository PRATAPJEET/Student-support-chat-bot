import streamlit as st
from google import genai
from google.genai import types
import google.genai.errors as errors
from dotenv import load_dotenv
import os

# Load API environment variables from the local .env configuration
load_dotenv()

def init_chatbot():
    """Initializes the Gemini API client interface safely searching all secret matrices."""
    api_key = None
    
    # 1. Try standard Streamlit Secrets dictionary access
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    # 2. Try secondary uppercase environment parsing format (Streamlit Cloud fallback)
    elif hasattr(st, "secrets") and st.secrets.get("GEMINI_API_KEY"):
        api_key = st.secrets.get("GEMINI_API_KEY")
    # 3. Try standard OS environment variable parsing (Local machine standard)
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        # Return None safely so it doesn't cause a Pydantic crash down the line
        return None
        
    return genai.Client(api_key=api_key)

def get_ai_stream_response(client, prompt_history, user_message):
    """
    Sends conversational context to the Gemini engine and handles streaming text feedback.
    Defensively parses history arrays to avoid structural schema validation errors.
    """
    # CRITICAL FALLBACK: If the client is None, display an actionable message instead of crashing!
    if client is None:
        yield "❌ **API Authentication Failed!** Streamlit Cloud cannot read your `GEMINI_API_KEY`. Please check your Streamlit Settings -> Secrets panel and verify the variable name matches perfectly."
        return
    
    try:
        # 1. Transform raw lists into strict Pydantic types.Content objects defensively
        formatted_contents = []
        for message in prompt_history:
            role = message.get("role", "user")
            
            # Defensive check: handle both 'parts' (new) and 'content' (old stale data) schemas
            if "parts" in message:
                content_text = message["parts"][0] if isinstance(message["parts"], list) else message["parts"]
            elif "content" in message:
                content_text = message["content"]
            else:
                continue
                
            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=str(content_text))]
                )
            )
        
        # 2. Append the latest live query to the target contents list
        formatted_contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=str(user_message))]
            )
        )
        
        # 3. Call generate_content_stream using the high-speed flash-lite model
        response_stream = client.models.generate_content_stream(
            model='gemini-3.1-flash-lite',
            contents=formatted_contents
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
            
    except errors.APIError as e:
        if e.code == 503:
            yield "⚠️ The AI server is experiencing heavy traffic spikes right now. Please wait a moment and resend your prompt!"
        else:
            yield f"An unexpected API connection error occurred: {e.message}"
    except Exception as e:
        yield f"System tracking error during streaming: {str(e)}"
import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """
    Initializes the Google GenAI Client cleanly using Streamlit secrets
    or local environment settings.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets.")
        st.stop()
        
    if "genai_client" not in st.session_state or force_rebuild:
        st.session_state.genai_client = genai.Client(api_key=api_key)

def get_ai_stream_response(current_prompt):
    """
    Fetches the full conversation response securely using the upgraded
    production Gemini 3.5 framework to clear the 404 new user restrictions.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    formatted_contents = []
    
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if msg["role"] in ["user", "model", "assistant"]:
                role = "model" if msg["role"] == "assistant" else msg["role"]
                formatted_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
    
    if not formatted_contents or formatted_contents[-1].parts[0].text != current_prompt:
        formatted_contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=current_prompt)]
            )
        )
    
    try:
        # Swapping out the locked model route for the active Gemini 3.5 production string
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=formatted_contents
        )
        
        if response.text:
            yield response.text
        else:
            yield "⚠️ I received an empty response from the AI engine."
                
    except Exception as e:
        print(f"Internal API Error Tracked: {str(e)}")
        yield f"⚠️ API Error Encountered: {str(e)}"
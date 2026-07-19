import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """
    Initializes the Google GenAI Client infrastructure securely using 
    Streamlit secrets or local environment variables.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets.")
        st.stop()
        
    # Initialize the modern developer client setup
    if "genai_client" not in st.session_state or force_rebuild:
        st.session_state.genai_client = genai.Client(api_key=api_key)

def get_ai_stream_response(current_prompt):
    """
    Formulates the full chat history stored in st.session_state.messages
    and passes it to the Gemini API so the bot maintains context and memory.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    
    # 1. Reconstruct the full historical conversation for the model
    formatted_contents = []
    
    # Check if there's an existing conversation tracked in session_state
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if msg["role"] in ["user", "model", "assistant"]:
                # The SDK strictly expects 'model' instead of 'assistant'
                role = "model" if msg["role"] == "assistant" else msg["role"]
                
                formatted_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
    
    # 2. Append the brand new prompt the user just sent if it isn't in history yet
    if not formatted_contents or formatted_contents[-1].parts[0].text != current_prompt:
        formatted_contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=current_prompt)]
            )
        )
    
    try:
        # 3. Send the entire back-and-forth history using the standardized stable flash engine
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=formatted_contents
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        # Log to server console while keeping UI clean
        print(f"Internal API Error Tracked: {str(e)}")
        yield f"⚠️ API Error Encountered: {str(e)}"
import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def init_chatbot(force_rebuild=False, custom_pdf_text=None):
    """
    Initializes the Google GenAI Client securely by routing communication
    through the stable 'v1' production API endpoint to support new AQ. keys.
    """
    # 1. Clear cloud environment overrides to protect the developer API key pathway
    cloud_env_vars = [
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_API_KEY",
        "GCLOUD_PROJECT"
    ]
    for var in cloud_env_vars:
        if var in os.environ:
            del os.environ[var]

    # 2. Fetch the correct user API key context
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Missing Gemini API Key. Please configure GEMINI_API_KEY in your Streamlit Secrets.")
        st.stop()
        
    # 3. Securely mount a pure developer client framework bound explicitly to the v1 stable engine
    if "genai_client" not in st.session_state or force_rebuild:
        st.session_state.genai_client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version='v1')
        )

def get_ai_stream_response(current_prompt):
    """
    Formulates the full chat history stored in st.session_state.messages
    and passes it to the Gemini API so the bot maintains context and memory.
    """
    if "genai_client" not in st.session_state:
        init_chatbot()
        
    client = st.session_state.genai_client
    
    # Reconstruct the full historical conversation for the model
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
    
    # Append the brand new prompt the user just sent if it isn't in history yet
    if not formatted_contents or formatted_contents[-1].parts[0].text != current_prompt:
        formatted_contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=current_prompt)]
            )
        )
    
    try:
        # Route the communication through the stable native flash engine on v1
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=formatted_contents
        )
        
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        print(f"Internal API Error Tracked: {str(e)}")
        yield f"⚠️ API Error Encountered: {str(e)}"
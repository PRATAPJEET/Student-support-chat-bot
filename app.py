import streamlit as st
import os
from dotenv import load_dotenv

# Import your fixed functions from chatbot.py
from chatbot import init_chatbot, get_ai_stream_response

# 1. Page Configuration
st.set_page_config(
    page_title="CampusAI Pro - Student Support Chatbot",
    page_icon="🎓",
    layout="wide"
)

# 2. Initialize Environment and API Client
load_dotenv()
client = init_chatbot()

# 3. Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. App UI Header
st.title("🎓 CampusAI Pro")
st.subheader("Your AI-Powered Academic Assistant")
st.write("Ask me anything about your courses, assignments, or programming tasks!")

# 5. Render Existing Chat History
for message in st.session_state.messages:
    # Handle the structure mismatch if parts dict is nested
    role = message["role"]
    content = message["parts"][0] if isinstance(message["parts"], list) else message["parts"]
    
    with st.chat_message(role):
        st.markdown(content)

# 6. Chat Input and Stream Loop Area
if prompt := st.chat_input("What is your question?"):
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "parts": [prompt]})

    # Generate assistant response container
    with st.chat_message("assistant"):
        placeholder = st.empty()
        resp = ""
        
        # Stream the response chunk by chunk with perfect alignment
        for chunk in get_ai_stream_response(client, st.session_state.messages[:-1], prompt):
            resp += chunk
            placeholder.markdown(resp)
            
    # Save full assistant response to history
    st.session_state.messages.append({"role": "assistant", "parts": [resp]})
import streamlit as st
import os
from dotenv import load_dotenv

# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(
    page_title="CampusAI Pro - Student Support Chatbot",
    page_icon="🎓",
    layout="wide"
)

# 2. Custom Layout Modules & Utilities Imports
# This pulls back your days of work from your project folder layout!
from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from chatbot import init_chatbot, get_ai_stream_response

# 3. Environment and Client Setup
load_dotenv()
client = init_chatbot()

# 4. Initialize Core Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Sets up your default home landing state

# 5. Render Your Workspace Sidebar Components
# This restores your modules list, PPT buttons, and academic tabs
with st.sidebar:
    render_sidebar()

# 6. Render Global UI Layout
render_header()

# 7. Page Routing Logic (Home Dashboard vs Module Tools)
if st.session_state.current_page == "Home":
    st.title("🎓 CampusAI Pro")
    st.subheader("Your AI-Powered Academic Assistant")
    st.write("Welcome back! Select a module from the sidebar or type a prompt below to begin.")
    
    # Render PPT / Processing utilities if active
    if st.button("📁 Process Lecture Presentations / PPT"):
        st.info("PPT Processor Module Activated. Upload your slides in the sidebar tab.")

# 8. Render Continuous Chat Session History
for message in st.session_state.messages:
    role = message["role"]
    content = message["parts"][0] if isinstance(message["parts"], list) else message["parts"]
    with st.chat_message(role):
        st.markdown(content)

# 9. Fixed Chat Input & Streaming Interface Block
if prompt := st.chat_input("What is your question?"):
    # Display the user's prompt instantly in the window
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add input history parameters safely
    st.session_state.messages.append({"role": "user", "parts": [prompt]})

    # Generate the streaming reply container with perfect indentation alignment
    with st.chat_message("assistant"):
        placeholder = st.empty()
        resp = ""
        
        # Pass all three required variables cleanly to clear the positional error
        for chunk in get_ai_stream_response(client, st.session_state.messages[:-1], prompt):
            resp += chunk
            placeholder.markdown(resp)  # Clean indentation tracking
            
    # Commit the fully parsed model reply to the session memory tracking array
    st.session_state.messages.append({"role": "assistant", "parts": [resp]})

# 10. Global Footer Layout
render_footer()
import os
import streamlit as st
from utils.helpers import load_css
from chatbot import init_chatbot, get_ai_stream_response

# 1. Page Configuration Setup
st.set_page_config(
    page_title="CampusAI Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize chatbot credentials early
init_chatbot()

# 2. Global State Management for Page Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Home"

# 3. Sidebar UI and Navigation Links
st.sidebar.title("🎓 CampusAI")
st.sidebar.caption("Your Intelligent Student Assistant")
st.sidebar.markdown("---")

theme_choice = st.sidebar.selectbox("Interface Theme", ["Dark Mode 🌙", "Light Mode 🌞"])
st.sidebar.markdown("---")

st.sidebar.subheader("🛠️ Navigation")
pages = [
    "Dashboard Home", 
    "AI Chat Thread", 
    "Student Success Support", 
    "Campus Knowledge Base", 
    "CS Programming Help", 
    "Chat with PDF Notes", 
    "Voice Audio Assistant"
]

for page in pages:
    # Highlights active page selection style
    label = f"🔴 {page}" if st.session_state.current_page == page else page
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.current_page = page

# 4. Dynamic Theme Style Injection (Fixes Washed-Out Light Mode)
if "Light Mode" in theme_choice:
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #F1F5F9 !important;
            }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
                color: #0F172A !important;
            }
            .stApp, [data-testid="stAppViewContainer"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }
            h1, h2, h3, p, span, div.stMarkdownContainer, [data-testid="stMarkdownContainer"] p {
                color: #0F172A !important;
            }
            [data-testid="stBaseButton-secondary"] {
                background-color: #E2E8F0 !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
            }
            [data-testid="stBaseButton-secondary"] * {
                color: #0F172A !important;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #0F172A !important;
            }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
                color: #F8FAFC !important;
            }
            .stApp, [data-testid="stAppViewContainer"] {
                background-color: #0B0F19 !important;
                color: #F8FAFC !important;
            }
            h1, h2, h3, p, span, div.stMarkdownContainer, [data-testid="stMarkdownContainer"] p {
                color: #F8FAFC !important;
            }
            [data-testid="stBaseButton-secondary"] {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
                border: 1px solid #334155 !important;
            }
            [data-testid="stBaseButton-secondary"] * {
                color: #F8FAFC !important;
            }
        </style>
    """, unsafe_allow_html=True)

# 5. Page Routing Controller Logic
if st.session_state.current_page == "Dashboard Home":
    st.title("Welcome to CampusAI Pro")
    st.write("Learn faster and navigate university workflows seamlessly with an integrated multi-module AI assistant framework.")
    
    # Render your home screen card grid setup here...
    st.subheader("Select a Specialized Intelligence Tool")

elif st.session_state.current_page == "AI Chat Thread":
    st.title("💬 General AI Chat Thread")
    
    # Initialize chat history array if not present for memory tracking
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages out of session_state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle incoming input prompt streams
    if prompt := st.chat_input("Ask anything..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in get_ai_stream_response(prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    # Placeholder routing fallback layout for secondary workspaces
    st.title(f"🛠️ {st.session_state.current_page}")
    st.info(f"The workspace context for {st.session_state.current_page} is successfully mounted.")
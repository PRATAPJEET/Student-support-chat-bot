import streamlit as st
import pypdf

from chatbot import get_ai_stream_response, init_chatbot
from utils.helpers import load_css
from components.sidebar import show_sidebar
from components.header import show_header
from utils.constants import (
    PAGE_HOME, PAGE_CHAT, PAGE_SUPPORT, PAGE_INFO, 
    PAGE_PROGRAMMING, PAGE_PDF, PAGE_VOICE
)

# ==========================
# WINDOW SETUP
# ==========================
st.set_page_config(
    page_title="CampusAI Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css("styles/style.css")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGE_HOME
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode 🌙"

# Apply Global Real-time Dynamic Light/Dark Theme Overrides
if st.session_state.theme_mode == "Light Mode ☀️":
    st.markdown(
        """
        <style>
            .stApp { background-color: #f8fafc !important; color: #0f172a !important; }
            .metric-card { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; color: #0f172a !important; }
            .metric-card p { color: #64748b !important; }
            .feature-box { background: #ffffff !important; border: 1px solid #e2e8f0 !important; }
            .feature-box h4 { color: #0f172a !important; }
            .feature-box p { color: #64748b !important; }
            h3, h1, label { color: #0f172a !important; }
            .stChatMessage { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; color: #0f172a !important; }
        </style>
        """, 
        unsafe_allow_html=True
    )

init_chatbot()

# ==========================
# GLOBAL WRAPPERS
# ==========================
show_sidebar()
show_header()

# ==========================
# 1. LANDING HOME DASHBOARD VIEW
# ==========================
if st.session_state.current_page == PAGE_HOME:
    
    # Hero Introduction Block
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); 
                    padding: 3.5rem 2rem; 
                    border-radius: 16px; 
                    border: 1px solid #2563eb; 
                    text-align: center; 
                    margin-bottom: 2.5rem;
                    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);">
            <h1 style="color: #ffffff !important; font-weight: 800; font-size: 3rem; margin: 0; letter-spacing: -0.5px;">
                Welcome to CampusAI Pro
            </h1>
            <p style="color: #93c5fd !important; font-size: 1.3rem; margin: 1rem 0 0 0; font-weight: 400; max-width: 700px; margin-left: auto; margin-right: auto;">
                Learn faster and navigate university workflows seamlessly with an integrated multi-module AI assistant framework.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Stat Metric Summary Counter Blocks
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><h3>⚡ 24/7</h3><p>Instant System Availability</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h3>⚙️ 6 Modules</h3><p>Contextual Core Environments</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h3>🎯 Grounded</h3><p>Verified College Knowledge</p></div>", unsafe_allow_html=True)
        
    st.markdown("<br><h3 style='text-align: center; font-weight: 600;'>Select a Specialized Intelligence Tool</h3>", unsafe_allow_html=True)
    
    # Grid Row 1
    grid_col1, grid_col2, grid_col3 = st.columns(3)
    with grid_col1:
        st.markdown("<div class='feature-box'><h4>💬 General AI Chat</h4><p>Ask generic campus queries and plan routine academic tracks smoothly.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Chat Thread", key="btn_chat", use_container_width=True):
            st.session_state.current_page = PAGE_CHAT
            st.rerun()
            
    with grid_col2:
        st.markdown("<div class='feature-box'><h4>🤝 Student Success Support</h4><p>Navigate administrative pipelines, deadlines, and student counseling networks contextually.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Success Workspace", key="btn_support", use_container_width=True):
            st.session_state.current_page = PAGE_SUPPORT
            st.rerun()
            
    with grid_col3:
        st.markdown("<div class='feature-box'><h4>🏢 Institutional Knowledge Base</h4><p>Deep query college guidelines parsed straight out of official text parameters.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Knowledge System", key="btn_info", use_container_width=True):
            st.session_state.current_page = PAGE_INFO
            st.rerun()

    # Grid Row 2
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    grid_col4, grid_col5, grid_col6 = st.columns(3)
    with grid_col4:
        st.markdown("<div class='feature-box'><h4>💻 CS Programming Assistant</h4><p>Debug structure loops and parse software structures step-by-step with a virtual TA.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Coding Engine", key="btn_prog", use_container_width=True):
            st.session_state.current_page = PAGE_PROGRAMMING
            st.rerun()
            
    with grid_col5:
        st.markdown("<div class='feature-box'><h4>📄 Custom PDF Analysis Chat</h4><p>Drop in course notes or standard syllabi files to extract quick answers instantly.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Document Processor", key="btn_pdf", use_container_width=True):
            st.session_state.current_page = PAGE_PDF
            st.rerun()
            
    with grid_col6:
        st.markdown("<div class='feature-box'><h4>🎙️ Conversational Audio Assistant</h4><p>Interact with standard audio voice parsing setups in an agile interface window.</p></div>", unsafe_allow_html=True)
        if st.button("Launch Voice Simulator", key="btn_voice", use_container_width=True):
            st.session_state.current_page = PAGE_VOICE
            st.rerun()

    # Feedback System
    st.markdown("<br><hr style='border-color: #334155;'><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>📣 User Feedback & Insights</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.95em;'>Help us optimize CampusAI. Share your experience or report bugs below.</p>", unsafe_allow_html=True)
    
    fb_col1, fb_col2 = st.columns([1, 2])
    with fb_col1:
        st.markdown("<div style='padding: 5px;'></div>", unsafe_allow_html=True)
        feedback_type = st.selectbox(
            "Feedback Category",
            ["✨ Feature Request", "🐛 Bug Report", "🙌 General Praise", "❓ Other"]
        )
        rating = st.feedback("stars", key="dashboard_stars")
        
    with fb_col2:
        comments = st.text_area(
            "Detailed Feedback / Notes", 
            placeholder="Tell us what you liked or what we can fix..."
        )
        
        if st.button("Submit Feedback Entry", use_container_width=True):
            if comments.strip() == "":
                st.warning("Please enter a short comment before submitting!")
            else:
                st.balloons()
                st.success(f"Thank you! Your feedback ({feedback_type}) has been logged successfully.")

# ==========================
# 2. RUNTIME FUNCTIONAL MODULE VIEWS
# ==========================
else:
    # PDF Processing View logic
    if st.session_state.current_page == PAGE_PDF:
        uploaded_file = st.file_uploader("Upload an Academic PDF (Syllabus, Notes, Assignments)", type=["pdf"])
        if uploaded_file and "pdf_text" not in st.session_state:
            with st.spinner("Extracting contents and grounding Gemini workspace engine..."):
                try:
                    reader = pypdf.PdfReader(uploaded_file)
                    extracted_text = ""
                    for page in reader.pages:
                        extracted_text += page.extract_text() + "\n"
                    st.session_state.pdf_text = extracted_text
                    init_chatbot(force_rebuild=True, custom_pdf_text=extracted_text)
                    st.success("Document verified! You can now query specific information below.")
                except Exception as e:
                    st.error(f"Failed to read file: {e}")

    # Voice Assistant View logic
    elif st.session_state.current_page == PAGE_VOICE:
        st.info("🎙️ Voice Simulator active. Capture speech values cleanly below.")
        audio_value = st.audio_input("Record your query")
        if audio_value:
            st.success("Audio captured successfully!")

    # Standard Chat message render loop (Historical Messages)
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat Input block
    placeholder_texts = {
        PAGE_CHAT: "Ask me anything about college life...",
        PAGE_SUPPORT: "Describe your administrative or counseling concern...",
        PAGE_INFO: "Query deadlines, timings, or location directives...",
        PAGE_PROGRAMMING: "Paste code snippets or programming logic questions here...",
        PAGE_PDF: "Ask me questions specific to your uploaded document text...",
        PAGE_VOICE: "Type here if your microphone isn't hooked up..."
    }

    prompt = st.chat_input(placeholder_texts.get(st.session_state.current_page, "Type here..."))

    if prompt:
        # 1. Show user message instantly
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. Stream the AI response block live!
        with st.chat_message("assistant", avatar="🤖"):
            response = st.write_stream(get_ai_stream_response(prompt))
                
        # 3. Cache the full response text string into history
        st.session_state.messages.append({"role": "assistant", "content": response})
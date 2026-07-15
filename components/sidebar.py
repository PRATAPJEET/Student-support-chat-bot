import streamlit as st
from utils.constants import (
    PAGE_HOME, PAGE_CHAT, PAGE_SUPPORT, PAGE_INFO, 
    PAGE_PROGRAMMING, PAGE_PDF, PAGE_VOICE
)
from chatbot import init_chatbot

def show_sidebar():
    """Renders highly styled workspace toggle controller with theme options."""
    with st.sidebar:
        st.markdown("## 🎓 CampusAI")
        st.markdown("<small style='color: #94a3b8;'>Your Intelligent Student Assistant</small>", unsafe_allow_html=True)
        st.markdown("---")
        
        # ==========================
        # INTERACTIVE THEME SWITCHER
        # ==========================
        st.markdown("### 🌗 Interface Theme")
        if "theme_mode" not in st.session_state:
            st.session_state.theme_mode = "Dark Mode 🌙"
            
        selected_theme = st.selectbox(
            "Select Theme",
            ["Dark Mode 🌙", "Light Mode ☀️"],
            index=0 if st.session_state.theme_mode == "Dark Mode 🌙" else 1,
            label_visibility="collapsed"
        )
        
        if selected_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = selected_theme
            st.rerun()

        st.markdown("---")
        st.markdown("### 🛠️ Navigation")
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = PAGE_HOME
            
        options_map = {
            PAGE_HOME: "🏠 Dashboard Home",
            PAGE_CHAT: "💬 AI Chat Thread",
            PAGE_SUPPORT: "🤝 Student Success Support",
            PAGE_INFO: "🏢 Campus Knowledge Base",
            PAGE_PROGRAMMING: "💻 CS Programming Help",
            PAGE_PDF: "📄 Chat with PDF Notes",
            PAGE_VOICE: "🎙️ Voice Audio Assistant"
        }
        
        selected_display = st.radio(
            label="Nav Options",
            options=list(options_map.values()),
            index=list(options_map.keys()).index(st.session_state.current_page),
            label_visibility="collapsed"
        )
        
        reverse_map = {v: k for k, v in options_map.items()}
        selected_token = reverse_map[selected_display]
        
        if selected_token != st.session_state.current_page:
            st.session_state.current_page = selected_token
            st.session_state.messages = []  
            if "pdf_text" in st.session_state:
                del st.session_state["pdf_text"]
            init_chatbot(force_rebuild=True)
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🧑‍💻 System Developer")
        st.markdown(
            "<div style='background-color: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155;'>"
            "<strong>Jeet Pratap</strong><br>"
            "<span style='font-size: 0.85em; color: #94a3b8;'>B.Tech Computer Science</span>"
            "</div>", 
            unsafe_allow_html=True
        )
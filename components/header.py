import streamlit as st
from utils.constants import PAGE_HOME

def show_header():
    """Renders contextual app header with integrated return-to-home actions."""
    current_page = st.session_state.get("current_page", PAGE_HOME)
    
    # Render layout header with navigation utilities when working inside a sub-module
    if current_page != PAGE_HOME:
        col_title, col_action = st.columns([3, 1])
        
        with col_title:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
                            padding: 1.2rem; 
                            border-radius: 12px; 
                            border: 1px solid #334155; 
                            display: flex;
                            align-items: center;">
                    <h2 style="color: #ffffff; font-weight: 700; margin: 0; font-size: 1.6rem;">🎓 {st.session_state.current_page} Workspace</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_action:
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            if st.button("🏠 Back to Home", use_container_width=True, key="header_home_btn"):
                st.session_state.current_page = PAGE_HOME
                st.session_state.messages = []  # Clear text threads smoothly
                st.rerun()
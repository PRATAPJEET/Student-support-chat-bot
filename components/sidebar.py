import streamlit as st

def render_sidebar():
    """
    Renders the navigation sidebar with automatic light/dark contrast mapping.
    """
    st.sidebar.title("🎓 CampusAI")
    st.sidebar.write("Your Intelligent Student Assistant")
    st.sidebar.markdown("---")
    
    # 1. The Theme Selector Dropdown
    theme_choice = st.sidebar.selectbox("Interface Theme", ["Light Mode 🌞", "Dark Mode 🌙"])
    st.sidebar.markdown("---")
    
    # 2. Dynamic high-contrast CSS Injection that respects the dropdown selection
    if "Light Mode" in theme_choice:
        st.markdown("""
            <style>
                /* Sidebar Background & Sidebar Elements contrast */
                [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                    background-color: #F1F5F9 !important;
                }
                [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
                    color: #0F172A !important;
                }
                
                /* Main Application Window Canvas Contrast */
                .stApp, [data-testid="stAppViewContainer"] {
                    background-color: #FFFFFF !important;
                    color: #0F172A !important;
                }
                h1, h2, h3, p, span, div.stMarkdownContainer {
                    color: #0F172A !important;
                }
                
                /* Grid Button Custom Contrast Fixes */
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
                /* Dark Mode styling logic defaults */
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
                h1, h2, h3, p, span, div.stMarkdownContainer {
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

    # 3. Sidebar Navigation Links
    st.sidebar.subheader("🛠️ Navigation")
    
    # Render your menu navigation choices down below
    # (Feel free to leave your existing button/page routing calls right here)
    if st.sidebar.button("🏠 Dashboard Home"):
        st.session_state.current_page = "Home"
    if st.sidebar.button("💬 AI Chat Thread"):
        st.session_state.current_page = "Chat"
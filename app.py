import os
import requests
import streamlit as st
from utils.helpers import load_css
from chatbot import init_chatbot, get_ai_stream_response
from streamlit_lottie import st_lottie

# 1. Page Configuration Setup
st.set_page_config(
    page_title="CampusAI Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize chatbot credentials early
init_chatbot()

# Helper function to fetch asset animations safely
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load a high-quality interactive AI tech assistant robot animation
lottie_robot = load_lottie_url("https://raw.githubusercontent.com/tuhinsamanta/Lottie-Animation-JSON-URL/main/robot.json")

# Initialize page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Home"

# 2. Sidebar UI and Navigation Links
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
    label = f"🔴 {page}" if st.session_state.current_page == page else page
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.current_page = page

# 3. Dynamic Theme Style Injection
if "Light Mode" in theme_choice:
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] { background-color: #F1F5F9 !important; }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #0F172A !important; }
            .stApp, [data-testid="stAppViewContainer"] { background-color: #FFFFFF !important; color: #0F172A !important; }
            h1, h2, h3, p, span, div.stMarkdownContainer, [data-testid="stMarkdownContainer"] p { color: #0F172A !important; }
            [data-testid="stBaseButton-secondary"] { background-color: #E2E8F0 !important; color: #0F172A !important; border: 1px solid #CBD5E1 !important; }
            [data-testid="stBaseButton-secondary"] * { color: #0F172A !important; }
            div[data-testid="metric-container"] { background-color: #F8FAFC !important; border: 1px solid #E2E8F0 !important; padding: 15px !important; border-radius: 10px !important; }
            .about-box { background-color: #F8FAFC !important; border-left: 5px solid #0078FF !important; padding: 20px !important; border-radius: 8px !important; margin-bottom: 25px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] { background-color: #0F172A !important; }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #F8FAFC !important; }
            .stApp, [data-testid="stAppViewContainer"] { background-color: #0B0F19 !important; color: #F8FAFC !important; }
            h1, h2, h3, p, span, div.stMarkdownContainer, [data-testid="stMarkdownContainer"] p { color: #F8FAFC !important; }
            [data-testid="stBaseButton-secondary"] { background-color: #1E293B !important; color: #F8FAFC !important; border: 1px solid #334155 !important; }
            [data-testid="stBaseButton-secondary"] * { color: #F8FAFC !important; }
            div[data-testid="metric-container"] { background-color: #1E293B !important; border: 1px solid #334155 !important; padding: 15px !important; border-radius: 10px !important; }
            .about-box { background-color: #1E293B !important; border-left: 5px solid #0078FF !important; padding: 20px !important; border-radius: 8px !important; margin-bottom: 25px !important; }
        </style>
    """, unsafe_allow_html=True)

# 4. Page Routing Controller Logic
if st.session_state.current_page == "Dashboard Home":
    
    # Hero Split: Title & About Section vs Floating Robot Animation
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    
    with col1:
        st.title("Welcome to CampusAI Pro")
        st.write("Learn faster and navigate university workflows seamlessly with an integrated multi-module AI assistant framework.")
        
        # 📌 RESTORED ABOUT SECTION WITH CLEAN CARD CONTAINER STYLE
        st.markdown("""
        <div class="about-box">
            <h4>💡 About the Developer</h4>
            <p><strong>I am Jeet Pratap, a B.Tech CSE enthusiast</strong> passionate about building intelligent systems, advanced algorithm engineering, and deep software infrastructure deployments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if lottie_robot:
            st_lottie(lottie_robot, height=220, speed=1, loop=True, quality="high", key="robot_assistant")
            
    st.markdown("---")
    
    # Metric Summary Row
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="⚡ System Status", value="24/7 Online")
    with m_col2:
        st.metric(label="⚙️ Active Modules", value="6 Specialized Engines")
    with m_col3:
        st.metric(label="🎯 Knowledge Integrity", value="Grounded Core")
        
    st.markdown("### Select a Specialized Intelligence Tool")
    
    # Beautiful Tool Grid System Layout
    grid_col1, grid_col2, grid_col3 = st.columns(3)
    
    with grid_col1:
        st.subheader("💬 General AI Chat")
        st.write("Ask generic campus queries and plan routine academic tracks smoothly.")
        if st.button("Launch Chat Thread", key="btn_chat", use_container_width=True):
            st.session_state.current_page = "AI Chat Thread"
            st.rerun()
            
    with grid_col2:
        st.subheader("🤝 Student Success")
        st.write("Navigate administrative pipelines, deadlines, and counseling networks contextually.")
        if st.button("Launch Success Workspace", key="btn_success", use_container_width=True):
            st.session_state.current_page = "Student Success Support"
            st.rerun()
            
    with grid_col3:
        st.subheader("🏢 Institutional Knowledge Base")
        st.write("Deep query college guidelines parsed straight out of official text parameters.")
        if st.button("Launch Knowledge System", key="btn_kb", use_container_width=True):
            st.session_state.current_page = "Campus Knowledge Base"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    grid_col4, grid_col5, grid_col6 = st.columns(3)
    
    with grid_col4:
        st.subheader("💻 CS Programming Assistant")
        st.write("Debug loops and parse software structures step-by-step with a virtual TA.")
        if st.button("Launch Coding Engine", key="btn_cs", use_container_width=True):
            st.session_state.current_page = "CS Programming Help"
            st.rerun()
            
    with grid_col5:
        st.subheader("📄 Custom PDF Analysis Chat")
        st.write("Drop in course notes or standard syllabi files to extract quick answers instantly.")
        if st.button("Launch Document Processor", key="btn_pdf", use_container_width=True):
            st.session_state.current_page = "Chat with PDF Notes"
            st.rerun()
            
    with grid_col6:
        st.subheader("🎙️ Conversational Audio Assistant")
        st.write("Interact with standard audio voice parsing setups in an agile interface window.")
        if st.button("Launch Voice Simulator", key="btn_voice", use_container_width=True):
            st.session_state.current_page = "Voice Audio Assistant"
            st.rerun()

elif st.session_state.current_page == "AI Chat Thread":
    st.title("💬 General AI Chat Thread")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
    st.title(f"🛠️ {st.session_state.current_page}")
    st.info(f"The workspace context for {st.session_state.current_page} is successfully mounted.")
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
        if r.status_code == 200:
            return r.json()
    except:
        return None

# Load interactive floating AI robot animation
lottie_robot = load_lottie_url("https://raw.githubusercontent.com/tuhinsamanta/Lottie-Animation-JSON-URL/main/robot.json")

# Initialize page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Home"

# 2. Sidebar UI Navigation
st.sidebar.title("🎓 CampusAI")
st.sidebar.caption("Your Intelligent Student Assistant")
st.sidebar.markdown("---")

# 📌 RESTORED BACK TO HOME DASHBOARD CONTROLLER BUTTON
if st.session_state.current_page != "Dashboard Home":
    if st.sidebar.button("🏠 Back to Home Dashboard", use_container_width=True, type="primary"):
        st.session_state.current_page = "Dashboard Home"
        st.rerun()
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
    label = f"💜 {page}" if st.session_state.current_page == page else page
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.current_page = page

# 3. Premium Cyber-Dark Lavender Style Injection with Full Hover Mechanics
st.markdown("""
    <style>
        /* Base Cyber Dark Canvas with Soft Purple Ambient Radial Glow */
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0B0F19 !important;
            background-image: radial-gradient(circle at 10% 20%, rgba(183, 148, 244, 0.05) 0%, transparent 40%), 
                              radial-gradient(circle at 90% 80%, rgba(183, 148, 244, 0.05) 0%, transparent 40%) !important;
            color: #F8FAFC !important;
        }
        
        /* Sidebar Polish */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] { 
            background-color: #0F172A !important; 
            border-right: 1px solid #1E293B !important;
        }
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] span { color: #F8FAFC !important; }
        
        /* Text Accent Styling Blocks */
        .hero-title { font-size: 3.2rem !important; font-weight: 800 !important; color: #B794F4 !important; margin-bottom: 5px !important; text-shadow: 0 0 15px rgba(183, 148, 244, 0.2); }
        .hero-subtitle { font-size: 2rem !important; font-weight: 700 !important; color: #F8FAFC !important; margin-bottom: 20px !important; }
        .hero-desc { font-size: 1.15rem !important; color: #94A3B8 !important; line-height: 1.7 !important; margin-bottom: 30px !important; }
        
        /* 📌 About Me Section Card Styling */
        .about-card { 
            background: #1E293B !important; 
            border-left: 5px solid #B794F4 !important; 
            padding: 20px !important; 
            border-radius: 12px !important; 
            margin-bottom: 25px !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }
        .about-card:hover {
            transform: scale(1.01) !important;
            box-shadow: 0 8px 20px rgba(183, 148, 244, 0.1) !important;
        }
        
        /* Interactive Counter Columns Layout */
        .stat-box { background: #1E293B !important; padding: 25px !important; border-radius: 16px !important; text-align: center !important; border: 1px solid #334155 !important; transition: all 0.3s ease !important; }
        .stat-box:hover { transform: translateY(-5px) !important; border-color: #B794F4 !important; box-shadow: 0 5px 15px rgba(183, 148, 244, 0.1) !important; }
        .stat-num { font-size: 2.2rem !important; font-weight: 800 !important; color: #B794F4 !important; margin-bottom: 5px !important; }
        .stat-lbl { font-size: 0.95rem !important; color: #94A3B8 !important; font-weight: 500 !important; }

        /* 🚀 Dynamic Lavender Hover Matrix for Grid Module Sections */
        .feature-card { 
            background: #1E293B !important; 
            padding: 30px 25px !important; 
            border-radius: 20px !important; 
            text-align: center !important; 
            border: 1px solid #334155 !important; 
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; 
            min-height: 230px !important; 
            margin-bottom: 15px !important; 
        }
        .feature-card:hover { 
            transform: translateY(-8px) !important; 
            box-shadow: 0 20px 25px -5px rgba(183, 148, 244, 0.15) !important; 
            border-color: #B794F4 !important; 
        }
        .feature-icon { font-size: 2.5rem !important; margin-bottom: 15px !important; display: inline-block !important; padding: 10px !important; background: #2D1B4E !important; border-radius: 50% !important; width: 70px !important; height: 70px !important; line-height: 50px !important; }
        .feature-title { font-size: 1.35rem !important; font-weight: 700 !important; color: #F8FAFC !important; margin-bottom: 10px !important; }
        .feature-desc { font-size: 0.95rem !important; color: #94A3B8 !important; line-height: 1.5 !important; }
        
        /* Button Hovers mapping */
        [data-testid="stBaseButton-secondary"] {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
            transition: all 0.25s ease !important;
        }
        [data-testid="stBaseButton-secondary"]:hover {
            border-color: #B794F4 !important;
            color: #B794F4 !important;
            background-color: #2D1B4E !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(183, 148, 244, 0.15) !important;
        }
        [data-testid="stBaseButton-secondary"] * { color: inherit !important; }
        
        /* Native Primary Action Button Fixes (Like Back to Dashboard) */
        [data-testid="stBaseButton-primary"] {
            background-color: #2D1B4E !important;
            color: #B794F4 !important;
            border: 1px solid #B794F4 !important;
            transition: all 0.25s ease !important;
        }
        [data-testid="stBaseButton-primary"]:hover {
            background-color: #B794F4 !important;
            color: #0F172A !important;
            box-shadow: 0 0 15px rgba(183, 148, 244, 0.4) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 4. Page Routing Logic
if st.session_state.current_page == "Dashboard Home":
    
    # --- HERO SPLIT LAYER ---
    col1, col2 = st.columns([1.3, 1], vertical_alignment="center")
    
    with col1:
        st.markdown('<div class="hero-title">AI Student Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Your Personal AI Learning Companion</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-desc">Learn faster with an intelligent AI assistant framework that can answer your academic questions, summarize notes, generate quizzes, write professional emails, and prepare smart study plans.</div>', unsafe_allow_html=True)
        
        # 📌 ABOUT ME SECTION COMPONENT
        st.markdown("""
        <div class="about-card">
            <span style="font-weight:700; font-size:1.1rem; display:block; margin-bottom:5px; color: #D6BCFA;">💡 About Me</span>
            <span style="font-size:0.98rem; opacity:0.9;">I am <strong>Jeet Pratap</strong>, a B.Tech CSE enthusiast passionate about engineering custom AI pipelines, context indexing engines, and modern UI dashboard frameworks.</span>
        </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns([1, 1])
        with btn_c1:
            if st.button("🔮 Start Chat Now", key="hero_start_chat", use_container_width=True):
                st.session_state.current_page = "AI Chat Thread"
                st.rerun()
        with btn_c2:
            st.link_button("🌐 View Portfolio", "https://github.com", use_container_width=True)

    with col2:
        if lottie_robot:
            st_lottie(lottie_robot, height=380, speed=1.2, loop=True, quality="high", key="premium_robot")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- PROMINENT COUNTER ROW DISPLAY ---
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.markdown('<div class="stat-box"><div class="stat-num">24/7</div><div class="stat-lbl">System Availability</div></div>', unsafe_allow_html=True)
    with s_col2:
        st.markdown('<div class="stat-box"><div class="stat-num">6</div><div class="stat-lbl">Smart Modules Loaded</div></div>', unsafe_allow_html=True)
    with s_col3:
        st.markdown('<div class="stat-box"><div class="stat-num">99%</div><div class="stat-lbl">Response Base Accuracy</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 10px; color: #D6BCFA;'>Everything you need in one smart dashboard.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Select a component module from below or use the sidebar layout controls to launch applications.</p>", unsafe_allow_html=True)
    
    # --- INTERACTIVE LAVENDER MODULE GRID CARDS ---
    grid1, grid2, grid3 = st.columns(3)
    
    with grid1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔮</div>
            <div class="feature-title">AI Chatbot</div>
            <div class="feature-desc">Ask questions instantly and handle continuous thread conversational topics seamlessly.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Chat Thread", key="go_chat", use_container_width=True):
            st.session_state.current_page = "AI Chat Thread"
            st.rerun()
            
    with grid2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <div class="feature-title">Success Advisor</div>
            <div class="feature-desc">Navigate administrative university pipelines, counselor guidelines, and active task tracking maps.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Success Pipeline", key="go_success", use_container_width=True):
            st.session_state.current_page = "Student Success Support"
            st.rerun()
            
    with grid3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Knowledge System</div>
            <div class="feature-desc">Deep query college rulebooks and administrative files parsed cleanly through context layers.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Institutional Base", key="go_kb", use_container_width=True):
            st.session_state.current_page = "Campus Knowledge Base"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    grid4, grid5, grid6 = st.columns(3)
    
    with grid4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💻</div>
            <div class="feature-title">CS Programming Assistant</div>
            <div class="feature-desc">Debug runtime code segments, evaluate algorithms, and analyze structure hierarchies.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Coding TA Engine", key="go_cs", use_container_width=True):
            st.session_state.current_page = "CS Programming Help"
            st.rerun()
            
    with grid5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Notes Summarizer</div>
            <div class="feature-desc">Drop in syllabi or extensive PDF course notes to run vector semantic extracts instantly.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Document Processor", key="go_pdf", use_container_width=True):
            st.session_state.current_page = "Chat with PDF Notes"
            st.rerun()
            
    with grid6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <div class="feature-title">Audio Assistant</div>
            <div class="feature-desc">Convert and parse incoming voice assets contextually through clean audio interfaces.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Voice Simulator", key="go_voice", use_container_width=True):
            st.session_state.current_page = "Voice Audio Assistant"
            st.rerun()

elif st.session_state.current_page == "AI Chat Thread":
    st.title("💬 General AI Chat Thread")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
    if prompt := st.chat_input("Ask anything..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            placeholder = st.empty()
            resp = ""
            for chunk in get_ai_stream_response(prompt):
                resp += chunk
                placeholder.markdown(resp + "▌")
            placeholder.markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})
else:
    st.title(f"🛠️ {st.session_state.current_page}")
    st.info(f"The workspace context for {st.session_state.current_page} is successfully mounted.")
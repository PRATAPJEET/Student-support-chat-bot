import os
import io
import requests
import streamlit as st
from utils.helpers import load_css
from chatbot import init_chatbot, get_ai_stream_response
from streamlit_lottie import st_lottie
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

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

# --- PPTX GENERATION ENGINE ---
def generate_pptx_stream():
    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 Widescreen Standard
    prs.slide_height = Inches(7.5)

    # Theme Color Palette Mapping
    BG_DARK = RGBColor(11, 15, 25)       # #0B0F19 Base Dark Canvas
    LAVENDER = RGBColor(183, 148, 244)   # #B794F4 Core Accent Title
    SOFT_PURPLE = RGBColor(214, 188, 250)# #D6BCFA Subtitle Highlight
    TEXT_LIGHT = RGBColor(248, 250, 252) # #F8FAFC Primary Content
    TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8 Secondary Subtexts

    def apply_dark_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_slide_header(slide, title_text):
        tx_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(11.833), Inches(1.0))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Helvetica'
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = LAVENDER

    blank_layout = prs.slide_layouts[6]

    # SLIDE 1: Title
    slide1 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide1)
    tx_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(4.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "🎓 CAMPUSAI PRO"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = LAVENDER
    p1.space_after = Pt(10)
    p2 = tf.add_paragraph()
    p2.text = "Advanced AI-Powered Multi-Module Student Assistant Terminal"
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(22)
    p2.font.color.rgb = SOFT_PURPLE
    p2.space_after = Pt(45)
    p3 = tf.add_paragraph()
    p3.text = "Presented by: Jeet Pratap (B.Tech CSE Enthusiast)\nProject Mentorship: Nikhil Sharma"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(16)
    p3.font.color.rgb = TEXT_LIGHT

    # SLIDE 2: Overview
    slide2 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide2)
    add_slide_header(slide2, "Project Overview")
    tx_box = slide2.shapes.add_textbox(Inches(0.75), Inches(2.0), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🤖 Core Architectural Intent:"
    p.font.name = 'Helvetica'
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SOFT_PURPLE
    p.space_after = Pt(14)
    bullets = [
        "Consolidates critical academic and programming operations into a unified dark-mode SaaS terminal ecosystem.",
        "Replaces slow legacy monolithic parsing logic with stateful context-grounded pipelines.",
        "Features an elegant, responsive structural grid map that responds smoothly to layout tracking states.",
        "Employs dynamic CSS animations and custom container overrides to ensure absolute code readability."
    ]
    for bullet in bullets:
        bp = tf.add_paragraph()
        bp.text = f"•  {bullet}"
        bp.font.name = 'Helvetica'
        bp.font.size = Pt(16)
        bp.font.color.rgb = TEXT_LIGHT
        bp.space_after = Pt(12)

    # SLIDE 3: Vision & Mission
    slide3 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide3)
    add_slide_header(slide3, "Vision & Strategic Mission")
    tx_box = slide3.shapes.add_textbox(Inches(0.75), Inches(2.0), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    sections = [
        ("👁️ System Vision", "To build a robust, ultra-responsive virtual intelligence core that lowers administrative knowledge block barriers and maps student operations instantly."),
        ("🎯 Core Mission Strategy", "Deliver zero-latency contextual lookups across complex university workflows. Empower computer science engineers to maximize core engineering focus by automating standard communication pipelines.")
    ]
    for title, desc in sections:
        p1 = tf.add_paragraph() if tf.text else tf.paragraphs[0]
        p1.text = title
        p1.font.name = 'Helvetica'
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = SOFT_PURPLE
        p1.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = 'Helvetica'
        p2.font.size = Pt(16)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(24)

    # SLIDE 4: Modules 1 & 2
    slide4 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide4)
    add_slide_header(slide4, "Core Modules 1 & 2")
    tx_box = slide4.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "🔮 Module 01: AI Chatbot Engine"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = SOFT_PURPLE
    p1.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "Processes real-time multi-turn strings using streaming token responses. Engineered to handle conversational threads seamlessly, enabling rapid code evaluation and query debugging formats."
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_after = Pt(30)
    p3 = tf.add_paragraph()
    p3.text = "🤝 Module 02: Student Success Support Advisor"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = SOFT_PURPLE
    p3.space_after = Pt(4)
    p4 = tf.add_paragraph()
    p4.text = "Maps administrative university guidelines, deadlines, and tracking pipelines contextually, giving students instant clarity on university compliance constraints."
    p4.font.name = 'Helvetica'
    p4.font.size = Pt(16)
    p4.font.color.rgb = TEXT_LIGHT

    # SLIDE 5: Modules 3 & 4
    slide5 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide5)
    add_slide_header(slide5, "Core Modules 3 & 4")
    tx_box = slide5.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "🏢 Module 03: Campus Knowledge Base Indexer"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = SOFT_PURPLE
    p1.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "Runs direct, optimized text indexing queries across regulatory college documentation, manuals, and rulebooks to deliver context-grounded data points with absolute integrity."
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_after = Pt(30)
    p3 = tf.add_paragraph()
    p3.text = "💻 Module 04: CS Programming Assistant TA"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = SOFT_PURPLE
    p3.space_after = Pt(4)
    p4 = tf.add_paragraph()
    p4.text = "Acts as an integrated virtual teaching assistant designed to parse algorithm structures, evaluate runtime execution loops, and offer step-by-step logic debugging."
    p4.font.name = 'Helvetica'
    p4.font.size = Pt(16)
    p4.font.color.rgb = TEXT_LIGHT

    # SLIDE 6: Modules 5 & 6
    slide6 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide6)
    add_slide_header(slide6, "Core Modules 5 & 6")
    tx_box = slide6.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "📄 Module 05: Notes Summarizer & Document Processor"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = SOFT_PURPLE
    p1.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "Ingests extensive study text files or syllabi parameters, utilizing contextual token extraction models to condense massive reference files into high-yield atomic summary blocks."
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_after = Pt(30)
    p3 = tf.add_paragraph()
    p3.text = "🎙️ Module 06: Conversational Audio Assistant"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = SOFT_PURPLE
    p3.space_after = Pt(4)
    p4 = tf.add_paragraph()
    p4.text = "Converts vocal audio input strings into highly coherent text maps to allow effortless hands-free query tracking right inside an agile dashboard UI viewport."
    p4.font.name = 'Helvetica'
    p4.font.size = Pt(16)
    p4.font.color.rgb = TEXT_LIGHT

    # SLIDE 7: Mentorship
    slide7 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide7)
    add_slide_header(slide7, "Mentorship & Engineering Acknowledgment")
    tx_box = slide7.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "👔 Project Mentorship: Nikhil Sharma"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = LAVENDER
    p1.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "Sincere architectural gratitude is extended to Nikhil Sharma for guiding core contextual parsing parameters, state machine logic boundaries, and general verification mechanics."
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_after = Pt(35)
    p3 = tf.add_paragraph()
    p3.text = "💻 Principal Architecture: Jeet Pratap"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = LAVENDER
    p3.space_after = Pt(4)
    p4 = tf.add_paragraph()
    p4.text = "Engineered entirely by Jeet Pratap, B.Tech Computer Science Engineering enthusiast focused on robust context routing pipelines and advanced interface configuration workflows."
    p4.font.name = 'Helvetica'
    p4.font.size = Pt(16)
    p4.font.color.rgb = TEXT_LIGHT

    # SLIDE 8: Closing
    slide8 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide8)
    add_slide_header(slide8, "Future Evolution Roadmap")
    tx_box = slide8.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(11.833), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    bullets_f = [
        "Voice Pipeline Integration: Deploying low-latency native vocal query loops.",
        "Deep Vector Processing: Scaling data storage matrices to ingest dense binary datasets.",
        "Performance Tracking Modules: Charting comprehensive query speed metrics and performance states.",
        "Production Scale Launch: Final routing to support high concurrent session contexts."
    ]
    for bullet in bullets_f:
        bp = tf.add_paragraph()
        bp.text = f"🚀  {bullet}"
        bp.font.name = 'Helvetica'
        bp.font.size = Pt(16)
        bp.font.color.rgb = TEXT_LIGHT
        bp.space_after = Pt(14)
    p_ty = tf.add_paragraph()
    p_ty.text = "\nTHANK YOU"
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.font.name = 'Helvetica'
    p_ty.font.size = Pt(32)
    p_ty.font.bold = True
    p_ty.font.color.rgb = LAVENDER

    # Save out to virtual memory buffer stream context
    ppt_stream = io.BytesIO()
    prs.save(ppt_stream)
    ppt_stream.seek(0)
    return ppt_stream

# 2. Sidebar UI Navigation
st.sidebar.title("🎓 CampusAI")
st.sidebar.caption("Your Intelligent Student Assistant")
st.sidebar.markdown("---")

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
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0B0F19 !important;
            background-image: radial-gradient(circle at 10% 20%, rgba(183, 148, 244, 0.05) 0%, transparent 40%), 
                              radial-gradient(circle at 90% 80%, rgba(183, 148, 244, 0.05) 0%, transparent 40%) !important;
            color: #F8FAFC !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] { 
            background-color: #0F172A !important; 
            border-right: 1px solid #1E293B !important;
        }
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] span { color: #F8FAFC !important; }
        
        .hero-title { font-size: 3.2rem !important; font-weight: 800 !important; color: #B794F4 !important; margin-bottom: 5px !important; text-shadow: 0 0 15px rgba(183, 148, 244, 0.2); }
        .hero-subtitle { font-size: 2rem !important; font-weight: 700 !important; color: #F8FAFC !important; margin-bottom: 20px !important; }
        .hero-desc { font-size: 1.15rem !important; color: #94A3B8 !important; line-height: 1.7 !important; margin-bottom: 30px !important; }
        
        .about-card { 
            background: #1E293B !important; 
            border-left: 5px solid #B794F4 !important; 
            padding: 20px !important; 
            border-radius: 12px !important; 
            margin-bottom: 25px !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }
        .about-card:hover { transform: scale(1.01) !important; box-shadow: 0 8px 20px rgba(183, 148, 244, 0.1) !important; }
        
        .stat-box { background: #1E293B !important; padding: 25px !important; border-radius: 16px !important; text-align: center !important; border: 1px solid #334155 !important; transition: all 0.3s ease !important; }
        .stat-box:hover { transform: translateY(-5px) !important; border-color: #B794F4 !important; box-shadow: 0 5px 15px rgba(183, 148, 244, 0.1) !important; }
        .stat-num { font-size: 2.2rem !important; font-weight: 800 !important; color: #B794F4 !important; margin-bottom: 5px !important; }
        .stat-lbl { font-size: 0.95rem !important; color: #94A3B8 !important; font-weight: 500 !important; }

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
        .feature-card:hover { transform: translateY(-8px) !important; box-shadow: 0 20px 25px -5px rgba(183, 148, 244, 0.15) !important; border-color: #B794F4 !important; }
        .feature-icon { font-size: 2.5rem !important; margin-bottom: 15px !important; display: inline-block !important; padding: 10px !important; background: #2D1B4E !important; border-radius: 50% !important; width: 70px !important; height: 70px !important; line-height: 50px !important; }
        .feature-title { font-size: 1.35rem !important; font-weight: 700 !important; color: #F8FAFC !important; margin-bottom: 10px !important; }
        .feature-desc { font-size: 0.95rem !important; color: #94A3B8 !important; line-height: 1.5 !important; }
        
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
    
    col1, col2 = st.columns([1.3, 1], vertical_alignment="center")
    
    with col1:
        st.markdown('<div class="hero-title">AI Student Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Your Personal AI Learning Companion</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-desc">Learn faster with an intelligent AI assistant framework that can answer your academic questions, summarize notes, generate quizzes, write professional emails, and prepare smart study plans.</div>', unsafe_allow_html=True)
        
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
            with st.spinner("Preparing PowerPoint file..."):
                ppt_data = generate_pptx_stream()
            st.download_button(
                label="📺 Download Presentation.pptx",
                data=ppt_data,
                file_name="CampusAI_Project_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )

    with col2:
        if lottie_robot:
            st_lottie(lottie_robot, height=380, speed=1.2, loop=True, quality="high", key="premium_robot")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
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
    
    grid1, grid2, grid3 = st.columns(3)
    
    with grid1:
        st.markdown('<div class="feature-card"><div class="feature-icon">🔮</div><div class="feature-title">AI Chatbot</div><div class="feature-desc">Ask questions instantly and handle continuous thread conversational topics seamlessly.</div></div>', unsafe_allow_html=True)
        if st.button("Open AI Chat Thread", key="go_chat", use_container_width=True):
            st.session_state.current_page = "AI Chat Thread"
            st.rerun()
            
    with grid2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🤝</div><div class="feature-title">Success Advisor</div><div class="feature-desc">Navigate administrative university pipelines, counselor guidelines, and active task tracking maps.</div></div>', unsafe_allow_html=True)
        if st.button("Open Success Pipeline", key="go_success", use_container_width=True):
            st.session_state.current_page = "Student Success Support"
            st.rerun()
            
    with grid3:
        st.markdown('<div class="feature-card"><div class="feature-icon">🏢</div><div class="feature-title">Knowledge System</div><div class="feature-desc">Deep query college rulebooks and administrative files parsed cleanly through context layers.</div></div>', unsafe_allow_html=True)
        if st.button("Open Institutional Base", key="go_kb", use_container_width=True):
            st.session_state.current_page = "Campus Knowledge Base"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    grid4, grid5, grid6 = st.columns(3)
    
    with grid4:
        st.markdown('<div class="feature-card"><div class="feature-icon">💻</div><div class="feature-title">CS Programming Assistant</div><div class="feature-desc">Debug runtime code segments, evaluate algorithms, and analyze structure hierarchies.</div></div>', unsafe_allow_html=True)
        if st.button("Open Coding TA Engine", key="go_cs", use_container_width=True):
            st.session_state.current_page = "CS Programming Help"
            st.rerun()
            
    with grid5:
        st.markdown('<div class="feature-card"><div class="feature-icon">📄</div><div class="feature-title">Notes Summarizer</div><div class="feature-desc">Drop in syllabi or extensive PDF course notes to run vector semantic extracts instantly.</div></div>', unsafe_allow_html=True)
        if st.button("Open Document Processor", key="go_pdf", use_container_width=True):
            st.session_state.current_page = "Chat with PDF Notes"
            st.rerun()
            
    with grid6:
        st.markdown('<div class="feature-card"><div class="feature-icon">🎙️</div><div class="feature-title">Audio Assistant</div><div class="feature-desc">Convert and parse incoming voice assets contextually through clean audio interfaces.</div></div>', unsafe_allow_html=True)
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
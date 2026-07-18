import streamlit as st
from utils.helpers import load_css
from components.sidebar import render_sidebar

# Initialize page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Render navigation sidebar
render_sidebar()

st.title("Welcome to CampusAI Pro")
st.write("Select a tool from the sidebar to get started.")

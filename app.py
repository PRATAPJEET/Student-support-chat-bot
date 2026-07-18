# Add this code to the absolute bottom of your app.py file
st.markdown("""
    <style>
        /* Automatically applies high-contrast styling adjustments for light mode elements */
        html[data-theme="light"] [data-testid="stSidebar"], 
        html[data-theme="light"] [data-testid="stSidebarContent"] {
            background-color: #F1F5F9 !important;
        }
        html[data-theme="light"] [data-testid="stSidebar"] *, 
        html[data-theme="light"] [data-testid="stSidebar"] span {
            color: #0F172A !important;
        }
        html[data-theme="light"] [data-testid="stBaseButton-secondary"] {
            background-color: #E2E8F0 !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }
        html[data-theme="light"] [data-testid="stBaseButton-secondary"] * {
            color: #0F172A !important;
        }
    </style>
""", unsafe_allow_html=True)
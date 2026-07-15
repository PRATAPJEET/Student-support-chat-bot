import streamlit as st


def load_css(css_file):
    """
    Load an external CSS file into the Streamlit app.
    """

    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
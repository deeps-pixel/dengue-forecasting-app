import streamlit as st
from components import theme

def render_background_rectangle():
    """
    Injects CSS to set the global background color of the application.
    Uses the theme's background light color (theme.D).
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #F8F9FA;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
from components import theme
import base64
import os

def render_header(title="Dengue Risk Monitoring and Prediction"):
    """
    Renders a fixed, full-width header with a logo on the left and centered title.
    """
    # Load and encode the logo
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
            logo_html = (
                f'<div class="header-logo-container">'
                f'  <a href="/" target="_self">'
                f'    <img src="data:image/png;base64,{logo_base64}" class="header-logo">'
                f'  </a>'
                f'</div>'
            )
    else:
        logo_html = ""

    st.markdown(
        f"""
        <style>
        .block-container {{
            padding-top: 110px !important; 
        }}
        
        .custom-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 120px;
            background-color: {theme.B};
            color: #FFFFFF;
            font-family: {theme.FONT};
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 1000;
        }}

        .header-logo-container {{
            position: absolute;
            left: 50px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
        }}

        .header-logo {{
            height: 85px;
            transition: transform 0.3s ease;
        }}

        .header-logo:hover {{
            transform: scale(1.05);
        }}

        .header-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0;
            text-align: center;
        }}
        
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        </style>
        <div class="custom-header">
            {logo_html}
            <div class="header-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

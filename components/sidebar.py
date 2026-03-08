import streamlit as st
from components import theme

def render_sidebar():
    with st.sidebar:
        # Styling for sidebar
        st.markdown(f"""
        <style>
        /* Fakes the sidebar being "under" the header 
           by making the top 120px transparent */
        section[data-testid="stSidebar"] {{
            background-color: transparent !important;
            background-image: linear-gradient(to bottom, transparent 120px, {theme.B} 120px) !important;
            border-right: none;
        }}

        /* The close/collapse button inside the sidebar */
        button[data-testid="stSidebarCollapseButton"] {{
            margin-top: 130px; /* 10px spacing below the 120px header */
            z-index: 1000002; 
        }}

        /* The open/expand button when the sidebar is collapsed */
        button[data-testid="stSidebarExpandButton"] {{
            margin-top: 130px; 
            z-index: 1000002;
        }}

        section[data-testid="stSidebar"] * {{
            color: white;
            font-family: {theme.FONT};
        }}

        .stButton button {{
            background-color: {theme.A};
            color: white;
            border-radius: {theme.R};
            font-weight: 700;
            width: 100%;
        }}

        .stButton button:hover {{
            background-color: {theme.C};
            color: {theme.B};
        }}
        </style>
        """, unsafe_allow_html=True)

        #st.markdown("## Navigation")

        # Push sidebar content down so it doesn't float into the transparent 120px header section
        st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

        # Create buttons for each page
        pages = ["Home", "Data Explorer", "Simulator", "Statistical Analysis"]
        
        if 'page' not in st.session_state:
            st.session_state['page'] = "Home"

        for p in pages:
            if st.button(p, key=f"btn_{p}"):
                st.session_state['page'] = p

    return st.session_state['page']

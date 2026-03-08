import streamlit as st
from components import theme
from components import ui_elements

def show():

    # Consolidated Flexible Content Card
    ui_elements.render_text_card([
        ('h2', "Welcome to the Dengue Risk Monitoring and Prediction Tool"),
        ('p', "This advanced analytical platform provides real-time insights and predictive modeling to help public health officials and researchers manage and mitigate dengue outbreaks."),
        ('h3', "Why Dengue Monitoring Matters?"),
        ('p', "Dengue is one of the fastest-growing mosquito-borne viral diseases in the world. Accurate monitoring allows for early detection of outbreaks, enabling timely interventions like mosquito control programs and hospital resource allocation."),
        ('h3', "What This Tool Does"),
        ('p', "Our tool combines historical epidemiological data with climate variables like temperature, rainfall, and humidity to visualize trends, simulate hypothetical scenarios, and perform rigorous statistical analysis.")
    ])
    
    # Themed Call-to-Action Line
    st.markdown(f"""
        <div style="
            text-align: center; 
            color: {theme.A}; 
            font-size: 1.8rem; 
            font-weight: 800; 
            margin-top: 1rem; 
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">
            Let's get Started!
        </div>
    """, unsafe_allow_html=True)

    # Navigation Buttons with simplified layout
    st.markdown('<div id="home-nav-box">', unsafe_allow_html=True)
    
    # Standard styling override (matching Statistical Analysis)
    ui_elements.apply_custom_button_style(container_id="home-nav-box", height="55px", font_size="1.1rem")
    
    # Row 1: Two buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Data Explorer", key="nav_explorer"):
            st.session_state['page'] = "Data Explorer"
            st.rerun()
    with col2:
        if st.button("Statistical Analysis", key="nav_analysis"):
            st.session_state['page'] = "Statistical Analysis"
            st.rerun()
            
    # Row 2: Centered Simulator button
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        # Since this button is also in #home-nav-box, it inherits the standard style
        if st.button("Simulator", key="nav_simulator", use_container_width=True):
            st.session_state['page'] = "Simulator"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

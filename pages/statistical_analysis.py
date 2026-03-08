import streamlit as st
from components import ui_elements

def show():
    # Header is handled globally in app.py

    ui_elements.render_info_card(
        "Statistical Analysis",
        """
        The statistical analysis module provides two primary avenues for understanding dengue risk. 
        Please select one of the models below to explore the detailed findings:
        """
    )

    # Wrapper div for scoping buttons
    st.markdown('<div id="analysis-nav-box">', unsafe_allow_html=True)
    
    # Selection buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Regression Model", use_container_width=True, key="btn_final_reg"):
            st.session_state['page'] = "Regression Model"
            st.rerun()
            
    with col2:
        if st.button("Risk Classification", use_container_width=True, key="btn_final_risk"):
            st.session_state['page'] = "Risk Classification"
            st.rerun()
    with col3:
        if st.button("Climate Insights", use_container_width=True, key="btn_final_climate"):
            st.session_state['page'] = "Climate Insights"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Apply the custom button style from ui_elements
    ui_elements.apply_custom_button_style(container_id="analysis-nav-box", height="50px", font_size="1.1rem")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Tip: You can return to this overview by selecting 'Statistical Analysis' from the sidebar.")

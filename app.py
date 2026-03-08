import streamlit as st

# MUST BE FIRST
st.set_page_config(
    page_title="Dengue Risk Monitoring",
    layout="wide"
)

from components.header import render_header
from components.sidebar import render_sidebar
from components.background_rect import render_background_rectangle
from pages import home, data_explorer, simulator, statistical_analysis, regression_model, risk_classification, climate_insights
from components import theme

# Sidebar navigation logic
page = render_sidebar()

# Page titles for the header
page_titles = {
    "Home": "Dengue Risk Dashboard",
    "Data Explorer": "Data Exploration",
    "Simulator": "Risk Simulation Model",
    "Statistical Analysis": "Statistical Analysis Overview",
    "Regression Model": "Statistical Analysis - Regression",
    "Risk Classification": "Statistical Analysis - Classification",
    "Climate Insights": "Statistical Analysis - Climate Insights"
}

# Persistent UI Elements
render_background_rectangle()
render_header()

# Routing
if page == "Home":
    home.show()
elif page == "Data Explorer":
    data_explorer.show()
elif page == "Simulator":
    simulator.show()
elif page == "Statistical Analysis":
    statistical_analysis.show()
elif page == "Regression Model":
    regression_model.show()
elif page == "Risk Classification":
    risk_classification.show()
elif page == "Climate Insights":
    climate_insights.show()
import streamlit as st
from components import theme, ui_elements, data_loader
import pandas as pd
import plotly.express as px
import numpy as np

def show():
    # Load and preprocess data
    df_raw = data_loader.load_dengue_data()
    df = data_loader.preprocess_data(df_raw)

    ui_elements.render_info_card(
        "Climate Insights & Impact Analysis",
        "Explore how specific climatic variables Rainfall, Temperature, and Humidity influence dengue transmission patterns. Select a factor below to view statistical correlations and monthly trends."
    )

    # Custom styling for the three grey impact buttons
    st.markdown(f"""
    <style>
    /* Targeting the specific horizontal block for the impact buttons */
    section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(button[key*="btn_impact"]) {{
        gap: 0px !important;
    }}
    
    section[data-testid="stMain"] div[data-testid="stHorizontalBlock"] .stButton > button {{
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: {theme.R} !important;
        height: 60px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
        width: 100% !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }}
    section[data-testid="stMain"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        background-color: #475569 !important;
        color: white !important;
        border-color: #475569 !important;
        z-index: 2;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Handle button clicks via session state
    if 'climate_view' not in st.session_state:
        st.session_state.climate_view = None

    # Button Row (Seamless buttons via CSS gap: 0)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("Rainfall Impact", use_container_width=True, key="btn_impact_rain"):
            st.session_state.climate_view = "Rainfall"
    with btn_col2:
        if st.button("Temperature Impact", use_container_width=True, key="btn_impact_temp"):
            st.session_state.climate_view = "Temperature"
    with btn_col3:
        if st.button("Humidity Impact", use_container_width=True, key="btn_impact_hum"):
            st.session_state.climate_view = "Humidity"

    view = st.session_state.climate_view
    
    if view is None:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
<div style="text-align: center; color: #94a3b8; padding: 100px 30px; border: 2px dashed #e2e8f0; border-radius: {theme.R};">
    <h3 style="color: #64748b;">Select a Climatic Factor Above to Begin Analysis</h3>
    <p>Choose Rainfall, Temperature, or Humidity to visualize their correlation with dengue outbreaks.</p>
</div>
""", unsafe_allow_html=True)
    else:
        # Subtitle for selected view
        st.markdown(f"<h2 style='text-align: center; color: {theme.B}; margin-top: 2rem;'>Analyzing {view} Association</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if view == "Rainfall":
            var = "Precipitation_avg"
            label = "Rainfall (mm/day)"
            unit = "mm/day"
            bins = [0, 5, 10, 15, 20, 30]
            bin_labels = ["0-5", "5-10", "10-15", "15-20", "20+"]
            
            interpret1 = "The scatter plot displays individual monthly data points, showing a positive correlation where increased rainfall frequency generally drives higher case volumes."
            interpret2 = "The distribution curve highlights that the majority of total dengue cases (~40-50%) are concentrated in the 0-5 mm/day rainfall range, signaling peak seasonal risk."

        elif view == "Temperature":
            var = "Temp_avg"
            label = "Temperature (°C)"
            unit = "°C"
            bins = [0, 25, 27, 29, 31, 100]
            bin_labels = ["<25", "25-27", "27-29", "29-31", ">31"]
            
            interpret1 = "The statistical correlation identifies an optimal 'Goldilocks' thermal zone. Cases peak significantly as temperatures rise towards 26°C before declining at extremes."
            interpret2 = "Nearly 60% of all recorded dengue cases occur when temperatures stay within the 25-27°C band, confirming this as the most critical window for viral transmission."

        else: # Humidity
            var = "Humidity_avg"
            label = "Humidity (%)"
            unit = "%"
            bins = [0, 70, 75, 80, 85, 90, 100]
            bin_labels = ["<70", "70-75", "75-80", "80-85", "85-90", ">90"]
            
            interpret1 = "Humidity levels over 80% show a dense cluster of high-case events, reflecting increased mosquito survival rates during more humid periods."
            interpret2 = "There is a massive spike here at the 85-90% humidity range, representing nearly 50% of cases which often overlap with peak monsoon cycles. Mosquitoes need high humidity to survive long enough to transmit the virus."

        # Prepare binned data for the line chart (Percentage Distribution)
        df_binned = df.copy()
        total_cases_sum = df_binned['Cases'].sum()
        df_binned['Range'] = pd.cut(df_binned[var], bins=bins, labels=bin_labels)
        
        # Calculate sum of cases per range and convert to percentage of global total
        df_trend = df_binned.groupby('Range', observed=True)['Cases'].sum().reset_index()
        df_trend['Percentage'] = (df_trend['Cases'] / total_cases_sum) * 100

        # Column 1: Charts Row
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig1 = px.scatter(df, x=var, y="Cases", 
                             title=f"Correlation: Cases vs {label}",
                             labels={var: label, "Cases": "Cases"},
                             trendline="ols",
                             color_discrete_sequence=[theme.A])
            fig1.update_layout(plot_bgcolor='#f8fafc', paper_bgcolor='white',
                              margin=dict(l=20, r=20, t=50, b=20),
                              xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
                              yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
                              title_x=0.5,
                              title_xanchor='center')
            st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            fig2 = px.line(df_trend, x="Range", y="Percentage",
                          title=f"% of Total Cases by {view} Range",
                          labels={"Range": f"{view} ({unit})", "Percentage": "% of Total Cases"},
                          color_discrete_sequence=[theme.B],
                          markers=True)
            # Make the line smoother and thicker
            fig2.update_traces(line=dict(width=4, shape='spline'), marker=dict(size=10))
            fig2.update_layout(plot_bgcolor='#f8fafc', paper_bgcolor='white',
                              margin=dict(l=20, r=20, t=50, b=20),
                              xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
                              yaxis=dict(showgrid=True, gridcolor='#e5e7eb', range=[0, df_trend['Percentage'].max() * 1.2]),
                              title_x=0.5,
                              title_xanchor='center')
            st.plotly_chart(fig2, use_container_width=True)

        # Column 2: Interpretation Row
        inter_col1, inter_col2 = st.columns(2)
        
        with inter_col1:
            ui_elements.render_compact_card("Correlation Detail", interpret1, height="200px")
            
        with inter_col2:
            ui_elements.render_compact_card("Incidence Distribution", interpret2, height="200px")

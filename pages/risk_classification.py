import streamlit as st
from components import ui_elements, theme, data_loader
import pandas as pd
import numpy as np
import plotly.express as px
import json

# --- Data Loading and Logic ---

@st.cache_data
def get_classification_results():
    """Performs risk classification using model-processed data (predictions)."""
    try:
        # Load and preprocess
        raw_df = data_loader.load_dengue_data()
        df_clean = data_loader.preprocess_data(raw_df)
        
        # Run regression to get "Processed" predicted values
        reg_results = data_loader.run_regression_analysis(df_clean)
        df = reg_results['df'] # Includes 'Predicted_Cases'
        
        # 1. Sum Predicted Cases by Province per Month (Sum across districts)
        monthly_province_sum = df.groupby(['Province', 'Year', 'Month'], observed=True).agg({
            'Predicted_Cases': 'sum',
            'Population': 'first', # This is province population
            'Temp_avg': 'mean',
            'Precipitation_avg': 'mean',
            'Humidity_avg': 'mean',
            'Cases': 'sum' # Also sum actual cases for reference
        }).reset_index()

        # 2. Average those monthly totals over time for each Province
        province_agg = monthly_province_sum.groupby('Province', observed=True).agg({
            'Predicted_Cases': 'mean', # This is now "Average Monthly Province Predicted Cases"
            'Population': 'first',
            'Temp_avg': 'mean',
            'Precipitation_avg': 'mean',
            'Humidity_avg': 'mean',
            'Cases': 'mean'
        }).reset_index()
        
        # 3. Calculate Incidence per 100k (using correct monthly totals) and round to nearest integer
        province_agg['incidence_per_100k'] = ((province_agg['Predicted_Cases'] / province_agg['Population']) * 100000).round().astype(int)
        
        # Determine risk levels using thresholds from the predicted distribution
        # We also round these to integers for user display
        low_t = int(round(province_agg['incidence_per_100k'].quantile(0.33)))
        high_t = int(round(province_agg['incidence_per_100k'].quantile(0.66)))

        def classify_risk(incidence):
            if incidence <= low_t: return 'Low Risk'
            elif incidence <= high_t: return 'Medium Risk'
            else: return 'High Risk'

        province_agg['risk_level'] = province_agg['incidence_per_100k'].apply(classify_risk)
        
        return {
            'province_risk': province_agg.to_dict('records'),
            'thresholds': (low_t, high_t),
            'raw_df': df # Handled as 'processed_df' in the logic below
        }
    except Exception as e:
        st.error(f"Error performing classification: {e}")
        return None

def show():
    results = get_classification_results()
    if not results:
        st.info("Check data availability in the components folder.")
        return
        
    province_risk_list = results['province_risk']
    low_t, high_t = results['thresholds']
    df = results['raw_df']

    # Page Header
    ui_elements.render_info_card(
        "Dengue Risk Classification",
        "This module categorizes Sri Lanka's provinces based on historical incidence rates and correlates them with key climatic drivers."
    )

    # Risk Colors
    color_high = "#e74c3c" # Red
    color_med  = "#f1c40f" # Yellow
    color_low  = "#2ecc71" # Green

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        ui_elements.render_subtle_heading("Geographical Risk Map")
        
        # --- Map Implementation ---
        district_id_map = {
            "Colombo": "LK11", "Gampaha": "LK12", "Kalutara": "LK13",
            "Kandy": "LK21", "Matale": "LK22", "Nuwara Eliya": "LK23",
            "Galle": "LK31", "Matara": "LK32", "Hambantota": "LK33",
            "Jaffna": "LK41", "Kilinochchi": "LK42", "Mannar": "LK43",
            "Vavuniya": "LK44", "Mulativu": "LK45",
            "Batticaloa": "LK51", "Ampara": "LK52", "Trincomalee": "LK53",
            "Kurunegala": "LK61", "Puttalam": "LK62",
            "Anuradhapura": "LK71", "Polonnaruwa": "LK72",
            "Badulla": "LK81", "Moneragala": "LK82",
            "Ratnapura": "LK91", "Kegalle": "LK92"
        }

        # Create a dictionary for quick lookup: Province -> {risk_level, color, climate}
        province_meta = {}
        for row in province_risk_list:
            p = row['Province']
            lvl = row['risk_level']
            clr = color_high if lvl == 'High Risk' else color_med if lvl == 'Medium Risk' else color_low
            province_meta[p] = {
                'lvl': lvl,
                'clr': clr,
                'temp': f"{row['Temp_avg']:.1f}°C",
                'rain': f"{row['Precipitation_avg']:.1f} mm",
                'hum': f"{row['Humidity_avg']:.1f}%"
            }

        # Map each district to its province's risk metadata
        district_mapping = df[['District', 'Province']].drop_duplicates()
        region_metadata = {}
        district_colors = {}
        
        for _, row in district_mapping.iterrows():
            d = row['District']
            p = row['Province']
            rid = district_id_map.get(d)
            if rid and p in province_meta:
                meta = province_meta[p]
                region_metadata[rid] = (
                    f"Risk: {meta['lvl']}<br>"
                    f"Avg Temp: {meta['temp']}<br>"
                    f"Avg Rain: {meta['rain']}<br>"
                    f"Avg Hum: {meta['hum']}"
                )
                district_colors[rid] = meta['clr']

        try:
            with open("assets/CountryMap/mapdata.js", "r", encoding="utf-8") as f:
                js_data = f.read()
            with open("assets/CountryMap/countrymap.js", "r", encoding="utf-8") as f:
                js_logic = f.read()
            
            hl_code = f"""
            <script>
            window.addEventListener('load', function() {{
                const colors = {json.dumps(district_colors)};
                const meta = {json.dumps(region_metadata)};
                
                if (typeof simplemaps_countrymap_mapdata !== 'undefined') {{
                    simplemaps_countrymap_mapdata.main_settings.background_color = "{theme.D}";
                    simplemaps_countrymap_mapdata.main_settings.background_transparent = "no";
                    
                    Object.keys(simplemaps_countrymap_mapdata.state_specific).forEach(id => {{
                        if (colors[id]) {{
                            simplemaps_countrymap_mapdata.state_specific[id].color = colors[id];
                            simplemaps_countrymap_mapdata.state_specific[id].hover_color = colors[id]; 
                            simplemaps_countrymap_mapdata.state_specific[id].description = meta[id];
                        }} else {{
                            simplemaps_countrymap_mapdata.state_specific[id].color = '#d1d5db';
                            simplemaps_countrymap_mapdata.state_specific[id].inactive = "yes";
                        }}
                    }});
                    // Trigger map update if necessary (usually simplemaps handles it on load)
                }}
            }});
            </script>
            """
            
            map_html = f"""
            <div id="map_container" style="position: relative; width: 100%; height: 700px; background-color: {theme.D}; border-radius: {theme.R};">
                <div id="map"></div>
            </div>
            <script>{js_data}</script>
            {hl_code}
            <script>{js_logic}</script>
            <style>
                body {{ background: {theme.D}; margin: 0; }}
                #map {{ width: 100%; height: 700px; }}
                #map svg path {{ stroke: #ffffff; stroke-width: 0.8; transition: opacity 0.2s ease; }}
                #map svg path:hover {{ opacity: 0.8; }}
                
                /* Aggressive removal of all Simplemaps trial/attribution markers */
                div[id*='simplemaps_attribution'], 
                #simplemaps_attribution,
                .simplemaps_attribution,
                a[href*='simplemaps.com'],
                span[style*='simplemaps'],
                text[style*='simplemaps'],
                path[id*='simplemaps_attribution'] {{ 
                    display: none !important; 
                    opacity: 0 !important; 
                    visibility: hidden !important;
                    height: 0 !important;
                    width: 0 !important;
                    pointer-events: none !important;
                }}
            </style>
            """
            st.components.v1.html(map_html, height=720)
        except Exception as e:
            st.error(f"Map rendering error: {e}")

    with col_right:
        ui_elements.render_subtle_heading("Risk Summary")
        
        # Categorize provinces by risk
        high_provinces = sorted([r['Province'] for r in province_risk_list if r['risk_level'] == 'High Risk'])
        med_provinces = sorted([r['Province'] for r in province_risk_list if r['risk_level'] == 'Medium Risk'])
        low_provinces = sorted([r['Province'] for r in province_risk_list if r['risk_level'] == 'Low Risk'])

        ui_elements.render_risk_card("High Risk Level", high_provinces, color_high)
        ui_elements.render_risk_card("Moderate Risk Level", med_provinces, color_med)
        ui_elements.render_risk_card("Low Risk Level", low_provinces, color_low)

    # Interpretation Box as a standard info card
    ui_elements.render_info_card(
        "How is Risk Classified?",
        f"""
        Risk levels are determined using the <b>33rd and 66th percentiles</b> of dengue incidence per 100,000 population. 
        This dynamic approach ensures risk is relative to overall disease trends.
        <br><br>
        <b>Classification Thresholds (Cases per 100k):</b><br>
        <span style="color:{color_low}; font-weight:700;">● LOW</span>: &le; {low_t:d} &nbsp;|&nbsp; 
        <span style="color:{color_med}; font-weight:700;">● MEDIUM</span>: {low_t:d} - {high_t:d} &nbsp;|&nbsp; 
        <span style="color:{color_high}; font-weight:700;">● HIGH</span>: > {high_t:d}
        """
    )

    # Separate card for Assumptions and Limitations
    st.markdown("<br>", unsafe_allow_html=True)
    
    ass_col1, ass_col2 = st.columns(2, gap="medium")
    with ass_col1:
        ui_elements.render_feature_card(
            "Assumptions",
            [
                "Dengue case data per district is accurate and complete.",
                "Population estimates reflect actual district populations.",
                "33rd and 66th percentiles are valid thresholds for relative risk.",
                "Risk levels represent the period analyzed (month/year).",
                "All areas within a district share the same risk level."
            ],
            border_color="#3498db",
            height="380px"
        )
    with ass_col2:
        ui_elements.render_feature_card(
            "Limitations",
            [
                "Cases may be underreported in some districts.",
                "Population data may be outdated or imprecise.",
                "Percentile-based risk is relative, not absolute.",
                "Environmental or socioeconomic factors are not included.",
                "No official national criteria exist for defining dengue risk levels; percentiles are used as a relative measure instead."
            ],
            border_color="#9b59b6",
            height="380px"
        )

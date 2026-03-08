import streamlit as st
from components import theme, ui_elements, data_loader
import pandas as pd
import numpy as np
import json

# Load & clean your dataset
df_raw = data_loader.load_dengue_data()
df = data_loader.preprocess_data(df_raw)

# Run your model (cached so it doesn't refit every time)
model_dict = data_loader.run_regression_analysis(df)

# Extract the models you need
nb_model = model_dict['nb_model']
metrics = model_dict['metrics']
irr = model_dict['irr']
poisson_model = model_dict['poisson_model']

#get risk classification
risk_classification = data_loader.run_risk_classification(df)


def show():
    # Persistent reset counter to force widget refreshes
    if 'sim_reset_counter' not in st.session_state:
        st.session_state.sim_reset_counter = 0
    cnt = st.session_state.sim_reset_counter

    ui_elements.render_info_card(
        "Dengue Case & Risk Simulator",
        "This simulator allows users to estimate the expected number of dengue cases and predicted risk level for a selected district based on climate conditions and population-adjusted statistical modelling."
    )

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
    Adjust the inputs below and run the simulation
</div>
""", unsafe_allow_html=True)


    # Reset Button at the top
    reset_col1, reset_col2 = st.columns([0.85, 0.15])
    with reset_col2:
        if st.button("Reset", key=f"sim_reset_btn_{cnt}", use_container_width=True):
            st.session_state.sim_reset_counter += 1
            st.session_state.simulation_run = False
            st.rerun()

    # Location Section
    ui_elements.render_subtle_heading("Location")
    
    col1, col2 = st.columns(2)
    provinces = sorted(df['Province'].unique().tolist())
    
    with col1:
        ui_elements.render_slider_heading("Province")
        selected_province = st.selectbox(
            "Province", 
            options=provinces,
            index=None,
            placeholder="Select Province",
            key=f"sim_prov_{cnt}",
            label_visibility="collapsed"
        )
        
    with col2:
        ui_elements.render_slider_heading("District")
        disabled = selected_province is None
        dist_options = []
        if not disabled:
            dist_options = sorted(df[df['Province'] == selected_province]['District'].unique().tolist())
            
        selected_district = st.selectbox(
            "District", 
            options=dist_options,
            index=None,
            placeholder="Select District",
            disabled=disabled,
            key=f"sim_dist_{cnt}",
            label_visibility="collapsed"
        )
    
    # Climatic Factors Section (Shown only if both are selected)
    if selected_province is not None and selected_district is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        ui_elements.render_subtle_heading("Climatic Factors")
        
        # Bi-directional sync functions
        def sync_t_box(): st.session_state[f"sim_temp_box_{cnt}"] = st.session_state[f"sim_temp_slider_{cnt}"]
        def sync_t_slider(): st.session_state[f"sim_temp_slider_{cnt}"] = st.session_state[f"sim_temp_box_{cnt}"]
        def sync_r_box(): st.session_state[f"sim_rain_box_{cnt}"] = st.session_state[f"sim_rain_slider_{cnt}"]
        def sync_r_slider(): st.session_state[f"sim_rain_slider_{cnt}"] = st.session_state[f"sim_rain_box_{cnt}"]
        def sync_h_box(): st.session_state[f"sim_hum_box_{cnt}"] = st.session_state[f"sim_hum_slider_{cnt}"]
        def sync_h_slider(): st.session_state[f"sim_hum_slider_{cnt}"] = st.session_state[f"sim_hum_box_{cnt}"]

        # Calculate global dataset min and max for slider extremes
        g_t_min, g_t_max = float(df['Temp_avg'].min()), float(df['Temp_avg'].max())
        g_r_min, g_r_max = float(df['Precipitation_avg'].min()), float(df['Precipitation_avg'].max())
        g_h_min, g_h_max = float(df['Humidity_avg'].min()), float(df['Humidity_avg'].max())
        
        # Calculate district averages for the starting points
        dist_data = df[df['District'] == selected_district]
        t_avg, r_avg, h_avg = float(dist_data['Temp_avg'].mean()), float(dist_data['Precipitation_avg'].mean()), float(dist_data['Humidity_avg'].mean())

        # If district changed, update session state to the new district's averages
        if f'last_district_{cnt}' not in st.session_state or st.session_state[f'last_district_{cnt}'] != selected_district:
            st.session_state[f'sim_temp_box_{cnt}'] = t_avg
            st.session_state[f'sim_temp_slider_{cnt}'] = t_avg
            st.session_state[f'sim_rain_box_{cnt}'] = r_avg
            st.session_state[f'sim_rain_slider_{cnt}'] = r_avg
            st.session_state[f'sim_hum_box_{cnt}'] = h_avg
            st.session_state[f'sim_hum_slider_{cnt}'] = h_avg
            st.session_state[f'last_district_{cnt}'] = selected_district

        # Initialize session state for climatic factors just in case
        if f'sim_temp_box_{cnt}' not in st.session_state: st.session_state[f'sim_temp_box_{cnt}'] = t_avg
        if f'sim_temp_slider_{cnt}' not in st.session_state: st.session_state[f'sim_temp_slider_{cnt}'] = t_avg
        if f'sim_rain_box_{cnt}' not in st.session_state: st.session_state[f'sim_rain_box_{cnt}'] = r_avg
        if f'sim_rain_slider_{cnt}' not in st.session_state: st.session_state[f'sim_rain_slider_{cnt}'] = r_avg
        if f'sim_hum_box_{cnt}' not in st.session_state: st.session_state[f'sim_hum_box_{cnt}'] = h_avg
        if f'sim_hum_slider_{cnt}' not in st.session_state: st.session_state[f'sim_hum_slider_{cnt}'] = h_avg

        # Temperature Section
        col_t1, col_t2 = st.columns([0.85, 0.15])
        with col_t1: ui_elements.render_slider_heading("Temperature (°C)")
        with col_t2: st.number_input("T", g_t_min, g_t_max, step=0.1, key=f"sim_temp_box_{cnt}", on_change=sync_t_slider, label_visibility="collapsed")
        st.slider("TS", g_t_min, g_t_max, step=0.1, key=f"sim_temp_slider_{cnt}", on_change=sync_t_box, label_visibility="collapsed")
        temp = st.session_state[f"sim_temp_slider_{cnt}"]
        
        # Rainfall Section
        col_r1, col_r2 = st.columns([0.85, 0.15])
        with col_r1: ui_elements.render_slider_heading("Rainfall (mm/day)")
        with col_r2: st.number_input("R", g_r_min, g_r_max, step=0.1, key=f"sim_rain_box_{cnt}", on_change=sync_r_slider, label_visibility="collapsed")
        st.slider("RS", g_r_min, g_r_max, step=0.1, key=f"sim_rain_slider_{cnt}", on_change=sync_r_box, label_visibility="collapsed")
        rain = st.session_state[f"sim_rain_slider_{cnt}"]

        # Humidity Section
        col_h1, col_h2 = st.columns([0.85, 0.15])
        with col_h1: ui_elements.render_slider_heading("Humidity (%)")
        with col_h2: st.number_input("H", g_h_min, g_h_max, step=0.1, key=f"sim_hum_box_{cnt}", on_change=sync_h_slider, label_visibility="collapsed")
        st.slider("HS", g_h_min, g_h_max, step=0.1, key=f"sim_hum_slider_{cnt}", on_change=sync_h_box, label_visibility="collapsed")
        humidity = st.session_state[f"sim_hum_slider_{cnt}"]
        
        if st.button("Run Simulation", type="primary", use_container_width=True, key=f"sim_run_btn_{cnt}"):
            with st.spinner("Running Simulation..."):
                # Extract static features
                population = data_loader.SRI_LANKA_POPULATION.get(selected_province, 1000000)
                elevation = df[df['District'] == selected_district]['Elevation'].iloc[0]
                
                # Construct input dataframe
                input_df = pd.DataFrame([{
                    'Temp_avg': temp,
                    'Precipitation_avg': rain,
                    'Humidity_avg': humidity,
                    'Elevation': elevation,
                    'District': selected_district,
                    'Population': population
                }])
                
                # Predict cases using the Negative Binomial Model
                st.session_state.predicted_cases = nb_model.predict(input_df, offset=np.log(input_df['Population'])).iloc[0]
                st.session_state.risk_level = risk_classification['province_risk'][risk_classification['province_risk']['Province'] == selected_province]['risk_level'].iloc[0]
                st.session_state.simulation_run = True

        # Display Results if simulation has been run
        if st.session_state.get('simulation_run', False):
            predicted_cases = st.session_state.predicted_cases
            risk_level = st.session_state.risk_level
            
            # Display Results
            st.markdown("<br>", unsafe_allow_html=True)
            ui_elements.render_subtle_heading("Simulation Results")
                
            # Contextual description card
            ui_elements.render_text_card([
                ('p', f"Based on the climatic conditions and specific geographic profile provided for <b>{selected_district}</b>, these are the predicted monthly average estimates and risk assessment for dengue outbreak activity.")
            ])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns([0.4, 0.6], gap="large")
            with res_col1:
                ui_elements.render_result_card("Expected Cases", f"{int(round(predicted_cases)):,}", color=theme.A, font_size="3rem", height="180px")
                st.markdown('<p style="color: #94a3b8; font-size: 0.85rem; text-align: center; margin-top: -15px;">Statistical Point Estimate</p>', unsafe_allow_html=True)
                
                st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

                # Predict risk level color
                if risk_level == 'Low Risk':
                    risk_color = '#10b981' # Green
                elif risk_level == 'Medium Risk':
                    risk_color = '#f59e0b' # Yellow/Amber
                else:
                    risk_color = '#ef4444' # Red
                
                ui_elements.render_result_card("Calculated Risk", risk_level, color=risk_color, value_color=risk_color, font_size="2.6rem", height="180px")

            with res_col2:
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
                rid = district_id_map.get(selected_district)
                
                try:
                    with open("assets/CountryMap/mapdata.js", "r", encoding="utf-8") as f:
                        js_data = f.read()
                    with open("assets/CountryMap/countrymap.js", "r", encoding="utf-8") as f:
                        js_logic = f.read()
                        
                    region_metadata = {}
                    if rid:
                        region_metadata[rid] = (f"Expected Cases: <b>{int(round(predicted_cases)):,}</b><br>"
                                                f"Temperature: {temp:.1f} °C<br>"
                                                f"Rainfall: {rain:.1f} mm/day<br>"
                                                f"Humidity: {humidity:.1f} %")
                        
                    hl_code = f"""
                    <script>
                    window.addEventListener('load', function() {{
                        const rid = "{rid}";
                        const meta = {json.dumps(region_metadata)};
                        const risk_color = "{risk_color}";
                        
                        if (typeof simplemaps_countrymap_mapdata !== 'undefined') {{
                            simplemaps_countrymap_mapdata.main_settings.background_color = "transparent";
                            simplemaps_countrymap_mapdata.main_settings.background_transparent = "yes";
                            
                            Object.keys(simplemaps_countrymap_mapdata.state_specific).forEach(id => {{
                                if (id !== rid) {{
                                    simplemaps_countrymap_mapdata.state_specific[id].color = '#d1d5db';
                                    simplemaps_countrymap_mapdata.state_specific[id].hover_color = '#d1d5db';
                                    simplemaps_countrymap_mapdata.state_specific[id].description = ""; 
                                    simplemaps_countrymap_mapdata.state_specific[id].name = ""; 
                                    simplemaps_countrymap_mapdata.state_specific[id].inactive = "yes";
                                }} else {{
                                    simplemaps_countrymap_mapdata.state_specific[id].color = risk_color;
                                    simplemaps_countrymap_mapdata.state_specific[id].hover_color = risk_color;
                                    simplemaps_countrymap_mapdata.state_specific[id].description = meta[id] || "";
                                }}
                            }});
                        }}
                    }});
                    </script>
                    """
                    
                    map_html = f"""
                    <div id="map_container" style="position: relative; width: 100%; height: 460px; background-color: transparent; border-radius: {theme.R}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden;">
                        <div id="map" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;"></div>
                    </div>
                    <script>{js_data}</script>
                    {hl_code}
                    <script>{js_logic}</script>
                    <style>
                        body {{ background: {theme.D}; margin: 0; display: flex; justify-content: center; }}
                        #map svg {{ max-height: 440px; width: auto !important; height: 100% !important; }}
                        #map svg path {{ stroke: #ffffff !important; stroke-width: 0.6 !important; transition: fill 0.2s ease; }}
                        
                        /* Aggressive removal of all Simplemaps attribution markers */
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
                    st.components.v1.html(map_html, height=470)
                except Exception as e:
                    st.error(f"Map rendering error: {e}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Predictions are based on historical patterns from 2019–2021 and provided climate conditions.")
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Run Again", use_container_width=True, type="secondary", key=f"sim_run_again_btn_{cnt}"):
                st.session_state.sim_reset_counter += 1
                st.session_state.simulation_run = False
                st.rerun()
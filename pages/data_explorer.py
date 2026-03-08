import streamlit as st
from components import ui_elements, theme, data_loader
import pandas as pd
import json
import plotly.express as px

# --- Data Loading (organized outside show() as requested) ---
df_raw = data_loader.load_dengue_data()
df = data_loader.preprocess_data(df_raw)

def show():
    # Helper for all years
    all_years = sorted(df['Year'].unique().tolist())
    
    # Initialize session state for filters
    if 'de_years' not in st.session_state:
        st.session_state.de_years = all_years
    if 'de_province' not in st.session_state:
        st.session_state.de_province = "All"
    if 'de_district' not in st.session_state:
        st.session_state.de_district = "All"
    if 'de_show_table' not in st.session_state:
        st.session_state.de_show_table = False

    # Filter Bar Helpers
    def year_filter():
        st.markdown('<span class="filter-label">Years:</span>', unsafe_allow_html=True)
        cols = st.columns(len(all_years))
        selected = []
        for i, y in enumerate(all_years):
            if cols[i].checkbox(str(y), value=y in st.session_state.de_years, key=f"de_y_{y}"):
                selected.append(y)
        st.session_state.de_years = selected

    def province_filter():
        provinces = ["All"] + sorted(df['Province'].unique().tolist())
        st.markdown('<span class="filter-label">Province:</span>', unsafe_allow_html=True)
        st.session_state.de_province = st.selectbox(
            "Select Province",
            options=provinces,
            index=provinces.index(st.session_state.de_province),
            label_visibility="collapsed",
            key="de_p_select"
        )

    def district_filter():
        if st.session_state.de_province == "All":
            dist_options = ["All"]
            disabled = True
        else:
            dist_options = ["All"] + sorted(df[df['Province'] == st.session_state.de_province]['District'].unique().tolist())
            disabled = False
        
        # Guard against district selection from another province
        if st.session_state.de_district not in dist_options:
            st.session_state.de_district = "All"
            
        st.markdown('<span class="filter-label">District:</span>', unsafe_allow_html=True)
        st.session_state.de_district = st.selectbox(
            "Select District",
            options=dist_options,
            index=dist_options.index(st.session_state.de_district),
            label_visibility="collapsed",
            key="de_d_select",
            disabled=disabled
        )

    def reset_button():
        st.markdown('<div style="margin-top: 42px;"></div>', unsafe_allow_html=True)
        if st.button("Reset", use_container_width=True, key="de_reset_btn"):
            st.session_state.de_years = all_years
            st.session_state.de_province = "All"
            st.session_state.de_district = "All"
            st.rerun()

    # Render Filter Bar
    ui_elements.render_filter_bar([
        year_filter,
        province_filter,
        district_filter,
        reset_button
    ], ratios=[1.5, 1.2, 1.2, 0.6], top_offset=0)

    # Filter Data
    df_filtered = df[df['Year'].isin(st.session_state.de_years)]
    if st.session_state.de_province != "All":
        df_filtered = df_filtered[df_filtered['Province'] == st.session_state.de_province]
    if st.session_state.de_district != "All":
        df_filtered = df_filtered[df_filtered['District'] == st.session_state.de_district]

    # Record Count Indicator
    count = len(df_filtered)
    st.markdown(f'<p style="color: {theme.C}; font-size: 0.95rem; padding-left: 15px; margin-top: -15px; margin-bottom: 25px;"><b>{count} record{"s" if count != 1 else ""} found.</b></p>', unsafe_allow_html=True)

    # Layout for Trends and Map
    chart_col, map_col = st.columns([1.1, 0.9], gap="large")

    with chart_col:
        ui_elements.render_subtle_heading("Monthly Dengue Trends")
        if not df_filtered.empty:
            # Revert to Multi-line chart per Year
            # Group by Year and Month
            chart_agg = df_filtered.groupby(['Year', 'Month'])['Cases'].sum().reset_index()
            
            # Map month to names
            month_abbr = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                          7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
            chart_agg['Month_Name'] = chart_agg['Month'].map(month_abbr)
            
            # Sort to ensure Jan-Dec order
            chart_agg = chart_agg.sort_values(['Year', 'Month'])
            
            # Use Plotly for fine control over interaction
            fig = px.line(
                chart_agg, 
                x="Month_Name", 
                y="Cases", 
                color="Year",
                #title="Monthly Dengue Trends",
                line_shape="linear",
                markers=True,
                labels={"Month_Name": "Month", "Cases": "Number of Cases"},
                template="plotly_white",
                color_discrete_sequence=[theme.A, theme.B, "#ffcc33"] 
            )
            
            # Refine Hover: Show only 'Number of Cases', hide Year/Month
            fig.update_traces(
                hovertemplate="Number of Cases: %{y}<extra></extra>"
            )
            
            # Interaction Tweaks: Hover ENABLED (Closest), Zoom DISABLED
            fig.update_layout(
                hovermode="closest",
                dragmode=False, # Disable drag/zoom
                xaxis=dict(fixedrange=True, categoryorder='array', categoryarray=list(month_abbr.values())),
                yaxis=dict(fixedrange=True),
                margin=dict(l=20, r=20, t=50, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                #title_x=0.5,
                #title_xanchor='center'
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            
            st.info("No data available for the trend chart.")

    with map_col:
        ui_elements.render_subtle_heading("Geographical Distribution")
        
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
        
        dist_cases = df_filtered.groupby('District', observed=True)['Cases'].sum().to_dict()
        
        if st.session_state.de_district != "All":
            hl_ids = [district_id_map.get(st.session_state.de_district)]
        elif st.session_state.de_province != "All":
            hl_ids = [district_id_map.get(d) for d in df[df['Province'] == st.session_state.de_province]['District'].unique() if d in district_id_map]
        else:
            hl_ids = [district_id_map.get(d) for d in df_filtered['District'].unique() if d in district_id_map]

        try:
            with open("assets/CountryMap/mapdata.js", "r", encoding="utf-8") as f:
                js_data = f.read()
            with open("assets/CountryMap/countrymap.js", "r", encoding="utf-8") as f:
                js_logic = f.read()
            
            region_metadata = {}
            for d, cases in dist_cases.items():
                rid = district_id_map.get(d)
                if rid:
                    region_metadata[rid] = f"Total Cases: {int(cases):,}"

            hl_code = f"""
            <script>
            window.addEventListener('load', function() {{
                const hlIds = {json.dumps(hl_ids)};
                const meta = {json.dumps(region_metadata)};
                
                if (typeof simplemaps_countrymap_mapdata !== 'undefined') {{
                    // Sync background with theme
                    simplemaps_countrymap_mapdata.main_settings.background_color = "{theme.D}";
                    simplemaps_countrymap_mapdata.main_settings.background_transparent = "no";
                    
                    Object.keys(simplemaps_countrymap_mapdata.state_specific).forEach(id => {{
                        if (!hlIds.includes(id)) {{
                            simplemaps_countrymap_mapdata.state_specific[id].color = '#d1d5db';
                            simplemaps_countrymap_mapdata.state_specific[id].hover_color = '#d1d5db';
                            simplemaps_countrymap_mapdata.state_specific[id].description = ""; 
                            simplemaps_countrymap_mapdata.state_specific[id].name = ""; 
                            simplemaps_countrymap_mapdata.state_specific[id].inactive = "yes";
                        }} else {{
                            // Use the name directly from mapdata.js which is already correct/updated
                            simplemaps_countrymap_mapdata.state_specific[id].color = '{theme.A}';
                            simplemaps_countrymap_mapdata.state_specific[id].hover_color = '#d16a3d';
                            simplemaps_countrymap_mapdata.state_specific[id].description = meta[id] || "No cases recorded";
                        }}
                    }});
                }}
            }});
            </script>
            """
            
            map_html = f"""
<div id="map_container" style="position: relative; width: 100%; height: 420px; background-color: {theme.D}; border-radius: {theme.R}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
    <div id="map"></div>
</div>
<script>{js_data}</script>
{hl_code}
<script>{js_logic}</script>
<style>
    body {{ background: {theme.D}; margin: 0; }}
    #map {{ width: 100%; height: 400px; }}
    #map svg path {{ stroke: #ffffff; stroke-width: 0.6; transition: fill 0.2s ease; }}
    
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
            st.components.v1.html(map_html, height=430)
        except Exception as e:
            st.error(f"Map rendering error: {e}")

    # --- Summary Metrics (Redesigned: 2-row White Premium Card) ---
    st.markdown("<br>", unsafe_allow_html=True)
    if not df_filtered.empty:
        total_cases = df_filtered['Cases'].sum()
        avg_cases = df_filtered['Cases'].mean()
        
        month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 
                     7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        month_sums = df_filtered.groupby('Month')['Cases'].sum()
        peak_month_num = month_sums.idxmax()
        peak_month_name = month_map.get(peak_month_num, f"Month {peak_month_num}")
        
        # Dynamic Metric 4: Context-aware
        m4_label = "Highest Affected District"
        m4_value = "—"

        if st.session_state.de_district != "All":
            # If a specific district is selected, show its % contribution to its province's total
            prov_total = df[(df['Province'] == st.session_state.de_province) & (df['Year'].isin(st.session_state.de_years))]['Cases'].sum()
            dist_total = df_filtered['Cases'].sum()
            if prov_total > 0:
                contribution = (dist_total / prov_total) * 100
                m4_label = "Contribution to Province"
                m4_value = f"{contribution:.1f}%"
        else:
            # Determine the highest district in the current filter
            district_sums = df_filtered.groupby('District', observed=True)['Cases'].sum()
            if not district_sums.empty:
                m4_value = district_sums.idxmax()

        metrics_data = [
            {'label': 'Total Cases', 'value': f"{int(total_cases):,}"},
            {'label': 'Average Monthly Cases', 'value': f"{int(round(avg_cases)):,}"},
            {'label': 'Peak Month', 'value': peak_month_name},
            {'label': m4_label, 'value': m4_value}
        ]
        ui_elements.render_summary_metrics_card(metrics_data)

    # Data Table Section
    st.markdown("<br>", unsafe_allow_html=True)
    table_label = "Hide Data Table" if st.session_state.de_show_table else "Show Data Table"
    if st.button(table_label, key="toggle_data_explorer_table"):
        st.session_state.de_show_table = not st.session_state.de_show_table
        st.rerun()
        
    if st.session_state.de_show_table:
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
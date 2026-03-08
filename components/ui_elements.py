import streamlit as st
from components import theme

def render_subpage_header(text):
    """Renders the centered subpage subtitle."""
    st.markdown(f"""
<style>
.subpage-header {{
    font-family: {theme.FONT};
    color: white;
    font-size: 1.2rem;
    margin-bottom: 20px;
    text-align: center;
    opacity: 0.9;
}}
</style>
<div class="subpage-header">{text}</div>
""", unsafe_allow_html=True)

def render_info_card(title, content):
    """Renders a white info card with an accent colored top border."""
    st.markdown(f"""
<style>
.info-card {{
    background-color: white;
    padding: 1.2rem 2.5rem 2.5rem 2.5rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align: center;
    border-top: 5px solid {theme.A};
    margin-bottom: 2rem;
}}
.info-card p {{
    color:#555; 
    font-size:1.1rem; 
    line-height:1.7;
    margin-bottom: 0;
}}
</style>
<div class="info-card">
    <h2 style="color:{theme.B}; margin-top:0;">{title}</h2>
    <p>{content}</p>
</div>
""", unsafe_allow_html=True)

def render_text_card(content_items):
    """
    Renders a white info card with highly flexible text content.
    content_items: list of tuples (tag_type, text_content)
    e.g. [('h2', 'Title'), ('p', 'Description')]
    """
    items_html = ""
    for tag, text in content_items:
        if tag == 'h2':
            items_html += f'<h2 style="color:{theme.B}; margin-top:0; margin-bottom: 0; font-size: 1.8rem; text-align: center;">{text}</h2>'
        elif tag == 'h3':
            items_html += f'<h3 style="color:{theme.B}; margin-top: 0rem; margin-bottom: 0rem; font-size: 1.15rem; font-weight: 600; text-align: center;">{text}</h3>'
        elif tag == 'p':
            items_html += f'<p style="color:#555; font-size:1.1rem; line-height:1.7; margin-bottom: 0; text-align: center;">{text}</p>'
    
    st.markdown(f"""
<style>
.flexible-text-card {{
    background-color: white;
    padding: 1.2rem 2.5rem 2.5rem 2.5rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-top: 5px solid {theme.A};
    margin-bottom: 2rem;
}}
</style>
<div class="flexible-text-card">
    {items_html}
</div>
""", unsafe_allow_html=True)

def render_compact_card(title, content, height="100%"):
    """Renders a smaller, centered info card with a hover effect and optional height."""
    st.markdown(f"""
<div class="compact-card" style="height: {height};">
    <h3>{title}</h3>
    <p>{content}</p>
</div>
<style>
.compact-card {{
    background-color: white;
    padding: 1.5rem;
    border-radius: {theme.R};
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    text-align: center;
    border-top: 4px solid {theme.A};
    margin-bottom: 1.5rem;
    cursor: default;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.compact-card h3 {{
    color: {theme.B};
    font-size: 1.15rem;
    margin-top: 0;
    margin-bottom: 0.6rem;
}}
.compact-card p {{
    color: #555;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 0;
}}
</style>
""", unsafe_allow_html=True)

def render_subtle_heading(text):
    """Renders a subtle, gray, capitalized heading."""
    st.markdown(f"""
<div style="
    font-family: {theme.FONT}; 
    font-weight: 600; 
    font-size: 1.1rem; 
    color: {theme.C}; 
    margin-top: 25px; 
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    text-align: center;
">
    {text}
</div>
""", unsafe_allow_html=True)

def render_metric_card(label, value, value_color=None, font_size="1.8rem", font_weight=800, height="100%"):
    """Renders a premium metric card with a colored top border."""
    if value_color is None:
        value_color = theme.A
    
    st.markdown(f"""
<div style="
    background-color: white;
    padding: 1.5rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    text-align: center;
    border-top: 5px solid {value_color};
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: {height};
    transition: transform 0.2s ease;
">
    <div style="color: #64748b; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
        {label}
    </div>
    <div style="font-size: {font_size}; color: {theme.B}; font-weight: {font_weight}; line-height: 1.1;">
        {value}
    </div>
</div>
""", unsafe_allow_html=True)

def render_result_card(label, value, color="#ef4444", value_color=None, font_size="2.4rem", font_weight=800, height="100%"):
    """Renders a results card with a colored left border and optional value font color."""
    if value_color is None:
        value_color = theme.B
    
    st.markdown(f"""
<div style="
    background-color: white;
    padding: 1.5rem 2rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border-left: 8px solid {color};
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: {height};
    margin-bottom: 1rem;
">
    <div style="color: #64748b; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
        {label}
    </div>
    <div style="font-size: {font_size}; color: {value_color}; font-weight: {font_weight}; line-height: 1.1;">
        {value}
    </div>
</div>
""", unsafe_allow_html=True)

def render_slider_heading(text):
    """Renders a distinct, semi-bold heading for climatic metric sliders."""
    st.markdown(f"""
<div style="
    font-family: {theme.FONT}; 
    font-weight: 700; 
    font-size: 1.1rem; 
    color: {theme.B}; 
    margin-bottom: 0px;
    display: inline-block;
">
    {text}
</div>
""", unsafe_allow_html=True)

def render_diagnostic_card(title, value, description):
    """Renders a detailed diagnostic card with title, value, and explanatory text."""
    st.markdown(f"""
<div style="
    background-color: white;
    padding: 1.5rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border-top: 4px solid {theme.A};
    height: 100%;
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
">
    <div style="color: {theme.B}; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
        {title}
    </div>
    <div style="font-size: 1.5rem; color: {theme.A}; font-weight: 800; margin-bottom: 15px;">
        {value}
    </div>
    <div style="color: #475569; font-size: 0.85rem; line-height: 1.5; flex-grow: 1;">
        {description}
    </div>
</div>
""", unsafe_allow_html=True)

def apply_custom_button_style(container_id="analysis-nav-box", height="50px", font_size="1.1rem"):
    """Injects CSS to style buttons within a specific container."""
    st.markdown(f"""
<style>
#{container_id} .stButton > button {{
    height: {height} !important;
    font-size: {font_size} !important;
    font-weight: 700 !important;
    background-color: {theme.A} !important;
    color: white !important;
    border-radius: {theme.R} !important;
    border: none !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    transition: all 0.2s ease !important;
}}
#{container_id} .stButton > button:hover {{
    background-color: {theme.B} !important;
    transform: scale(1.02) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

def apply_main_button_style():
    """Applies a premium, large, bold style to buttons in the main content area."""
    st.markdown(f"""
<style>
/* target only buttons in the main section, not the sidebar */
section[data-testid="stMain"] .stButton > button {{
    height: 80px !important;
    width: 100% !important;
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    background-color: {theme.A} !important;
    color: white !important;
    border-radius: {theme.R} !important;
    border: none !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.12) !important;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}}

section[data-testid="stMain"] .stButton > button:hover {{
    background-color: {theme.B} !important;
    color: white !important;
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: 0 15px 30px rgba(0,0,0,0.25) !important;
}}

section[data-testid="stMain"] .stButton > button:active {{
    transform: translateY(-3px) scale(0.97) !important;
}}
</style>
""", unsafe_allow_html=True)

def render_interpretation_card(text, height="100%", color=None, show_border=True):
    """Renders a card for graphical interpretations with vertical centering and optional height."""
    if color is None:
        color = theme.B
    
    # Define border style based on show_border toggle
    border_style = f"border-left: 5px solid {color};" if show_border else "border: none;"
    
    st.markdown(f"""
<div style="
    background-color: white; 
    padding: 1.5rem; 
    border-radius: {theme.R}; 
    {border_style}
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    height: {height};
    display: flex;
    flex-direction: column;
    justify-content: center;
">
    <p style="color: #4A5568; font-size: 0.95rem; line-height: 1.6; margin: 0;">
        {text}
    </p>
</div>
""", unsafe_allow_html=True)

def render_feature_card(title, items, border_color=None, height="100%"):
    """Renders a card with a title and a list of items, used for assumptions/limitations."""
    if border_color is None:
        border_color = theme.A
    
    items_html = "".join([f"<li>{item}</li>" for item in items])
    
    st.markdown(f"""
<div style="background: #fff; padding: 1.5rem; border-radius: {theme.R}; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 5px solid {border_color}; height: {height};">
    <h4 style="color: {border_color}; margin-top:0; font-weight: 700;">{title}</h4>
    <ul style="color: #555; font-size: 0.9rem; padding-left: 20px; line-height: 1.6; margin-bottom: 0;">
        {items_html}
    </ul>
</div>
""", unsafe_allow_html=True)

def render_styled_box(title, content, bg_color="#f0f7ff", border_color="#3498db", text_color="#2980b9"):
    """Renders a styled box with a background color and left border."""
    st.markdown(f"""
<div style="background-color: {bg_color}; padding: 1.5rem; border-radius: {theme.R}; border-left: 5px solid {border_color}; margin-bottom: 25px;">
    <h4 style="color: {text_color}; margin-top: 0; font-size: 1.1rem; font-weight: 700;">{title}</h4>
    <p style="color: #34495e; font-size: 0.95rem; margin: 0; line-height: 1.6;">
        {content}
    </p>
</div>
""", unsafe_allow_html=True)

def render_risk_card(title, provinces, color):
    """Renders a card for risk levels with a list of provinces."""
    if not provinces:
        items_html = '<div style="color: #94a3b8; font-style: italic; font-size: 0.9rem;">No provinces in this category</div>'
    else:
        items_html = "".join([f'<div style="color: {theme.B}; margin-bottom: 6px; font-weight: 600; font-size: 1.05rem; display: flex; align-items: center;"><span style="color: {color}; margin-right: 8px; font-size: 1.2rem;">•</span>{p}</div>' for p in provinces])
    
    st.markdown(f"""
<div style="
    background-color: white; 
    padding: 1.2rem; 
    border-radius: {theme.R}; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    border-left: 8px solid {color};
    margin-bottom: 1rem;
">
    <h4 style="color: {color}; margin-top: 0; margin-bottom: 1rem; text-transform: uppercase; font-size: 0.85rem; font-weight: 800; letter-spacing: 0.5px;">{title}</h4>
    <div style="display: flex; flex-direction: column;">
        {items_html}
    </div>
</div>
""", unsafe_allow_html=True)

def render_summary_metrics_card(metrics):
    """
    Renders a 2x2 grid of metrics in a premium white card.
    metrics: list of dicts [{'label': 'Total Cases', 'value': '1,234'}, ...]
    Expects exactly 4 metrics for the 2x2 grid.
    """
    if len(metrics) < 4:
        # Fallback for fewer metrics
        cols = st.columns(len(metrics))
        for i, m in enumerate(metrics):
            with cols[i]:
                render_metric_card(m['label'], m['value'])
        return

    st.markdown(f"""
<style>
.explorer-metric-card {{
    background-color: white;
    padding: 2.5rem;
    border-radius: {theme.R};
    box-shadow: 0 4px 12px rgba(0,0,0,0.05), 0 10px 30px rgba(0,0,0,0.08); 
    border-top: 5px solid {theme.A};
    margin-bottom: 2rem;
}}
.explorer-metric-row {{
    display: flex;
    justify-content: flex-start;
    gap: 40px;
    margin-bottom: 30px;
}}
.explorer-metric-row:last-child {{ 
    margin-bottom: 0;
}}
.metric-box {{ flex: 1; }}
.header-bold {{ 
    color: {theme.B}; 
    font-size: 1.05rem; 
    text-transform: uppercase; 
    font-weight: 800; 
    margin-bottom: 12px;
}}
.value-bold {{ 
    font-size: 2.4rem; 
    font-weight: 900; 
    color: {theme.A}; 
    line-height: 1.1;
}}
</style>
<div class="explorer-metric-card">
    <div class="explorer-metric-row">
        <div class="metric-box">
            <div class="header-bold">{metrics[0]['label']}</div>
            <div class="value-bold">{metrics[0]['value']}</div>
        </div>
        <div class="metric-box">
            <div class="header-bold">{metrics[1]['label']}</div>
            <div class="value-bold">{metrics[1]['value']}</div>
        </div>
    </div>
    <div class="explorer-metric-row">
        <div class="metric-box">
            <div class="header-bold">{metrics[2]['label']}</div>
            <div class="value-bold">{metrics[2]['value']}</div>
        </div>
        <div class="metric-box">
            <div class="header-bold">{metrics[3]['label']}</div>
            <div class="value-bold">{metrics[3]['value']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

def render_math_card(title, latex_formula):
    """Renders a single cohesive card with a title and a centered LaTeX formula."""
    st.markdown(f"""
<div style="
    background-color: white; 
    padding: 2rem; 
    border-radius: {theme.R}; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    border-top: 5px solid {theme.A}; 
    margin-bottom: 2rem;
    text-align: center;
">
    <h3 style="color: {theme.B}; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.15rem;">{title}</h3>
    <div style="font-size: 1.2rem; color: {theme.B}; padding: 10px 0;">
        $${latex_formula}$$
    </div>
</div>
""", unsafe_allow_html=True)

def render_filter_bar(widgets, ratios=None, top_offset=0):
    """
    Renders a full-width, horizontal sticky filter bar.
    Uses CSS to style the st.columns as a single contained unit.
    """
    # Inject CSS for filter bar targeting the next horizontal block
    st.markdown(f"""
<style>
/* Target the horizontal block created by st.columns following this anchor */
div:has(> #filter-bar-anchor) + div [data-testid="stHorizontalBlock"] {{
    background-color: {theme.C} !important;
    padding: 5px 20px !important;
    border-radius: {theme.R} !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    position: sticky !important;
    top: {top_offset}px !important;
    z-index: 99 !important;
    margin-top: -55px !important; /* Minimal gap from header */
    border: 1px solid rgba(0,0,0,0.05) !important;
    display: flex !important;
}}

.filter-label {{
    color: {theme.B} !important;
    font-weight: 700 !important;
    margin-right: 8px !important;
    white-space: nowrap;
    font-size: 0.9rem;
}}

/* Ensure align-center for all widgets inside the columns */
div:has(> #filter-bar-anchor) + div [data-testid="stHorizontalBlock"] > div {{
    display: flex !important;
    align-items: center !important;
}}

.stCheckbox, .stSelectbox, .stButton {{
    margin-bottom: 0px !important;
}}
</style>
<div id="filter-bar-anchor"></div>
""", unsafe_allow_html=True)

    # Create columns for the widgets
    n_widgets = len(widgets)
    if ratios is None or len(ratios) != n_widgets:
        ratios = [1] * n_widgets
    
    cols = st.columns(ratios)

    # Render each widget into its column
    for i, widget_func in enumerate(widgets):
        with cols[i]:
            widget_func()
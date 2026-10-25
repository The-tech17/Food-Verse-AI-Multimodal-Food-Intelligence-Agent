"""
Food Verse AI - Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3)
Evaluates perishable raw items for surface texture, discoloration, wrinkling,
and mold spores to classify freshness stage and provide actionable food safety directives.
"""

import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from modules.sample_data import SAMPLE_FRESHNESS, get_sample_image

def render_freshness_gauge(score: int, stage: str):
    """Renders a gauge chart illustrating freshness status."""
    color_map = {
        "Fresh": "#10B981",
        "Moderately Fresh": "#F59E0B",
        "Spoiled": "#F43F5E"
    }
    bar_color = color_map.get(stage, "#10B981")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Freshness Integrity Index</b>", 'font': {'color': "#F8FAFC", 'size': 14}},
        number={'suffix': "%", 'font': {'color': bar_color, 'size': 28, 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#94A3B8"},
            'bar': {'color': bar_color},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(244, 63, 94, 0.2)'},
                {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94A3B8"),
        margin=dict(l=15, r=15, t=30, b=10),
        height=200
    )
    return fig

def render_freshness_tab(ai_engine):
    """Main renderer for Food Freshness & Spoilage Diagnostic."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">🥑 Food Freshness & Spoilage Diagnostic</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            AI-powered microbiological inspection evaluating surface texture decay, enzymatic discoloration, skin turgor wrinkling, and fungal mycelium presence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title">🔍 Inspect Perishable Raw Food</p>', unsafe_allow_html=True)
        
        # Preset buttons for 1-click test
        st.caption("⚡ Quick Demo Presets:")
        preset_cols = st.columns(3)
        selected_preset = None
        with preset_cols[0]:
            if st.button("🍓 Moldy Fruit", key="fresh_preset_mold", use_container_width=True):
                selected_preset = "spoiled_fruit"
        with preset_cols[1]:
            if st.button("🍎 Fresh Apple", key="fresh_preset_apple", use_container_width=True):
                selected_preset = "fresh_apple"
        with preset_cols[2]:
            if st.button("🍌 Ripe Banana", key="fresh_preset_banana", use_container_width=True):
                selected_preset = "ripe_banana"

        if selected_preset:
            st.session_state["tab2_active_preset"] = selected_preset
            st.session_state["tab2_uploaded_file"] = None

        food_category = st.selectbox(
            "Food Category:",
            ["Fresh Fruits & Berries", "Leafy Greens & Vegetables", "Raw Poultry & Red Meat", "Dairy & Cheese", "Fresh Seafood"],
            index=0
        )

        uploaded_file = st.file_uploader(
            "Upload food surface photo (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="freshness_uploader"
        )
        if uploaded_file:
            st.session_state["tab2_uploaded_file"] = uploaded_file
            st.session_state["tab2_active_preset"] = None
            
        display_img = None
        preset_key = st.session_state.get("tab2_active_preset", "spoiled_fruit")
        
        if st.session_state.get("tab2_uploaded_file") is not None:
            try:
                display_img = Image.open(st.session_state["tab2_uploaded_file"])
            except Exception as e:
                st.error(f"Error opening image: {e}")
        else:
            display_img = get_sample_image(preset_key)
            
        if display_img:
            st.image(display_img, caption="Surface Diagnostic Subject", use_container_width=True)
            
        analyze_clicked = st.button("🔬 Perform Spoilage Diagnostic", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_output:
        if analyze_clicked or "tab2_result" not in st.session_state:
            with st.spinner("🔬 Performing cellular texture & fungal spore optical diagnostics..."):
                if st.session_state.get("tab2_uploaded_file") is not None and ai_engine.provider != "Demo":
                    result = ai_engine.analyze_freshness(display_img, food_category)
                else:
                    result = SAMPLE_FRESHNESS.get(preset_key, SAMPLE_FRESHNESS["spoiled_fruit"])
                st.session_state["tab2_result"] = result
        else:
            result = st.session_state["tab2_result"]
            
        item_name = result.get("item_name", "Perishable Sample")
        stage = result.get("freshness_stage", "Moderately Fresh")
        score = result.get("freshness_score", 60)
        verdict = result.get("food_safety_verdict", "Consume with caution")
        badge = result.get("safety_badge", "INSPECT")
        shelf_life = result.get("remaining_shelf_life", "1-2 days")
        
        # Color styling
        if stage == "Fresh":
            badge_class = "fv-status-fresh"
            card_border = "#10B981"
            directive_class = "fv-callout-success"
        elif stage == "Moderately Fresh":
            badge_class = "fv-status-moderate"
            card_border = "#F59E0B"
            directive_class = "fv-callout-warning"
        else:
            badge_class = "fv-status-spoiled"
            card_border = "#F43F5E"
            directive_class = "fv-callout-danger"
            
        st.markdown(f"""
        <div class="fv-card" style="border-color:{card_border};">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin:0; font-size:1.3rem; color:#FFFFFF;">{item_name}</h3>
                    <div style="margin-top:6px; display:flex; gap:8px;">
                        <span class="fv-status-pill {badge_class}">CLASSIFICATION: {stage.upper()}</span>
                        <span class="fv-tag" style="background:rgba(255,255,255,0.06); color:#E2E8F0;">Shelf Life: {shelf_life}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge and safety directive banner
        gauge_fig = render_freshness_gauge(score, stage)
        st.plotly_chart(gauge_fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="fv-callout {directive_class}" style="margin-top:-10px;">
            <div style="font-size:1.05rem; font-weight:800; text-transform:uppercase; letter-spacing:0.04em;">
                🛡️ Safety Directive: {badge}
            </div>
            <div style="margin-top:4px; font-size:0.92rem;">
                <b>Verdict:</b> {verdict}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Four-pillar physical inspection grid
        st.markdown('<p style="font-size:0.85rem; font-weight:700; color:#94A3B8; text-transform:uppercase; margin-top:16px;">BIOMORPHOMETRIC INSPECTION PILLARS:</p>', unsafe_allow_html=True)
        
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f"""
            <div class="fv-card" style="padding:14px; margin-bottom:12px;">
                <b style="color:#38BDF8;">🔍 Surface Texture & Firmness</b>
                <p style="font-size:0.85rem; color:#CBD5E1; margin:6px 0 0 0;">{result.get('texture_analysis', 'Normal firmness')}</p>
            </div>
            <div class="fv-card" style="padding:14px; margin-bottom:12px;">
                <b style="color:#F59E0B;">🍂 Discoloration & Oxidation</b>
                <p style="font-size:0.85rem; color:#CBD5E1; margin:6px 0 0 0;">{result.get('discoloration_index', 'Minimal browning')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with p2:
            mold_detected = "POSITIVE" in result.get('mold_detection', '').upper()
            mold_color = "#F43F5E" if mold_detected else "#10B981"
            st.markdown(f"""
            <div class="fv-card" style="padding:14px; margin-bottom:12px;">
                <b style="color:#A78BFA;">💧 Wrinkling & Turgor Pressure</b>
                <p style="font-size:0.85rem; color:#CBD5E1; margin:6px 0 0 0;">{result.get('wrinkling_turgor', 'Normal hydration')}</p>
            </div>
            <div class="fv-card" style="padding:14px; margin-bottom:12px; border-color:{mold_color};">
                <b style="color:{mold_color};">🍄 Mold & Microbial Spores</b>
                <p style="font-size:0.85rem; color:#CBD5E1; margin:6px 0 0 0;">{result.get('mold_detection', 'None detected')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Actionable advice & preservation protocols
        tab_actions, tab_storage = st.tabs(["📋 Immediate Action Protocol", "❄️ Food Science Preservation Tips"])
        
        with tab_actions:
            advice_list = result.get("actionable_advice", [])
            for item in advice_list:
                st.markdown(f"- **Guidance:** {item}")
                
        with tab_storage:
            tips = result.get("preservation_tips", [])
            for tip in tips:
                st.markdown(f"- **Protocol:** {tip}")

"""
Food Verse AI - Tab 3: Kitchen Hygiene & Food Safety Compliance (Epic 4)
Audits commercial kitchen environments for chef hat/hairnet compliance, glove usage,
surface sanitization, and cross-contamination hazards to compute overall Compliance Score.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from modules.sample_data import SAMPLE_KITCHEN, get_sample_image

def render_compliance_meter(score: int, grade: str):
    """Renders a half-donut gauge chart for Kitchen Hygiene Compliance."""
    color = "#10B981" if score >= 85 else ("#F59E0B" if score >= 70 else "#F43F5E")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"<b>Compliance Grade: {grade}</b>", 'font': {'color': "#F8FAFC", 'size': 14}},
        number={'suffix': "%", 'font': {'color': color, 'size': 32, 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#94A3B8"},
            'bar': {'color': color},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 60], 'color': 'rgba(244, 63, 94, 0.2)'},
                {'range': [60, 80], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94A3B8"),
        margin=dict(l=15, r=15, t=30, b=10),
        height=210
    )
    return fig

def render_hygiene_tab(ai_engine):
    """Main renderer for Kitchen Hygiene & Food Safety Compliance."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">🧼 Kitchen Hygiene & Food Safety Compliance</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            HACCP & FDA Food Code automated inspection agent for PPE compliance, hair restraints, food-safe glove protocols, and cross-contamination hazards.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title">📹 Commercial Kitchen Audit Input</p>', unsafe_allow_html=True)
        
        # Preset buttons for 1-click test
        st.caption("⚡ Quick Demo Presets:")
        preset_cols = st.columns(3)
        selected_preset = None
        with preset_cols[0]:
            if st.button("🍳 Hot Line Station", key="hygiene_preset_hot", use_container_width=True):
                selected_preset = "kitchen_hygiene"
        with preset_cols[1]:
            if st.button("🥩 Prep Cross-Contam", key="hygiene_preset_raw", use_container_width=True):
                selected_preset = "kitchen_hygiene"
        with preset_cols[2]:
            if st.button("🥐 Bakery Station", key="hygiene_preset_bake", use_container_width=True):
                selected_preset = "kitchen_hygiene"

        if selected_preset:
            st.session_state["tab3_active_preset"] = selected_preset
            st.session_state["tab3_uploaded_file"] = None

        facility_type = st.selectbox(
            "Facility / Workstation Type:",
            ["Commercial Restaurant Hot Line", "Cold Prep / Salad Bar Station", "Meat & Poultry Butchery", "Catering & Event Assembly", "Bakery & Pastry Station"],
            index=0
        )

        uploaded_file = st.file_uploader(
            "Upload kitchen photo or video frame (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp", "mp4"],
            key="hygiene_uploader"
        )
        if uploaded_file:
            st.session_state["tab3_uploaded_file"] = uploaded_file
            st.session_state["tab3_active_preset"] = None
            
        display_img = None
        preset_key = st.session_state.get("tab3_active_preset", "kitchen_hygiene")
        
        if st.session_state.get("tab3_uploaded_file") is not None:
            # Check if video or image
            if uploaded_file.name.endswith(".mp4"):
                st.video(uploaded_file)
                # Fallback representative image for model inference
                display_img = get_sample_image("kitchen_hygiene")
            else:
                try:
                    display_img = Image.open(st.session_state["tab3_uploaded_file"])
                except Exception as e:
                    st.error(f"Error opening image: {e}")
        else:
            display_img = get_sample_image(preset_key)
            
        if display_img and not (uploaded_file and uploaded_file.name.endswith(".mp4")):
            st.image(display_img, caption="Commercial Kitchen Inspection Viewport", use_container_width=True)
            
        analyze_clicked = st.button("📋 Run HACCP Hygiene Inspection", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_output:
        if analyze_clicked or "tab3_result" not in st.session_state:
            with st.spinner("🤖 Computer Vision Inspector auditing PPE, sanitary state, and cross-contamination vectors..."):
                if st.session_state.get("tab3_uploaded_file") is not None and ai_engine.provider != "Demo" and display_img:
                    result = ai_engine.analyze_kitchen_hygiene(display_img, facility_type)
                else:
                    result = SAMPLE_KITCHEN.get(preset_key, SAMPLE_KITCHEN["kitchen_hygiene"])
                st.session_state["tab3_result"] = result
        else:
            result = st.session_state["tab3_result"]
            
        score = result.get("compliance_score", 85)
        grade = result.get("compliance_grade", "Grade B+")
        status = result.get("hygiene_status", "Operational")
        
        status_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 65 else "#F43F5E")
        
        st.markdown(f"""
        <div class="fv-card" style="border-color:{status_color};">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin:0; font-size:1.3rem; color:#FFFFFF;">{result.get('title', 'Kitchen Compliance Audit')}</h3>
                    <div style="margin-top:6px;">
                        <span class="fv-tag" style="background:rgba(16, 185, 129, 0.15); color:#34D399; font-weight:700;">{status.upper()}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Meter chart
        meter_fig = render_compliance_meter(score, grade)
        st.plotly_chart(meter_fig, use_container_width=True)
        
        # 4 Core Indicators
        indicators = result.get("indicators", {})
        hat_stat = indicators.get("chef_hat_hairnet", {}).get("status", "Compliant")
        glove_stat = indicators.get("glove_usage", {}).get("status", "Partial")
        clean_stat = indicators.get("sanitization_state", {}).get("status", "Good")
        cross_stat = indicators.get("cross_contamination", {}).get("status", "Safe")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="fv-card" style="padding:14px; margin-bottom:10px;">
                <b style="color:#38BDF8;">🧑‍🍳 Hairnet / Restraint:</b> 
                <span class="fv-tag fv-tag-safe" style="margin-left:6px;">{hat_stat}</span>
                <p style="font-size:0.83rem; color:#CBD5E1; margin:6px 0 0 0;">{indicators.get('chef_hat_hairnet', {}).get('details', '')}</p>
            </div>
            <div class="fv-card" style="padding:14px; margin-bottom:10px;">
                <b style="color:#F59E0B;">🧤 Glove & Hand Protocol:</b> 
                <span class="fv-tag" style="margin-left:6px; background:rgba(245, 158, 11, 0.15); color:#FCD34D;">{glove_stat}</span>
                <p style="font-size:0.83rem; color:#CBD5E1; margin:6px 0 0 0;">{indicators.get('glove_usage', {}).get('details', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="fv-card" style="padding:14px; margin-bottom:10px;">
                <b style="color:#10B981;">🧼 Sanitization State:</b> 
                <span class="fv-tag fv-tag-safe" style="margin-left:6px;">{clean_stat}</span>
                <p style="font-size:0.83rem; color:#CBD5E1; margin:6px 0 0 0;">{indicators.get('sanitization_state', {}).get('details', '')}</p>
            </div>
            <div class="fv-card" style="padding:14px; margin-bottom:10px;">
                <b style="color:#F43F5E;">☣️ Cross-Contamination:</b> 
                <span class="fv-tag fv-tag-allergen" style="margin-left:6px;">{cross_stat}</span>
                <p style="font-size:0.83rem; color:#CBD5E1; margin:6px 0 0 0;">{indicators.get('cross_contamination', {}).get('details', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Itemized Violation Logs
        st.markdown('<p style="font-size:0.85rem; font-weight:700; color:#94A3B8; text-transform:uppercase; margin-top:14px;">ITEMIZED AUDIT VIOLATION LOGS:</p>', unsafe_allow_html=True)
        violations = result.get("violations", [])
        if violations:
            for v in violations:
                sev = v.get("severity", "Minor")
                sev_color = "#F43F5E" if sev == "Critical" else ("#F59E0B" if sev == "Major" else ("#38BDF8" if sev == "Minor" else "#10B981"))
                st.markdown(f"""
                <div class="fv-card" style="padding:12px 16px; margin-bottom:10px; border-left:4px solid {sev_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b>{v.get('issue', 'Issue')}</b>
                        <span style="font-size:0.75rem; font-weight:700; color:{sev_color}; text-transform:uppercase;">{sev} ({v.get('code', 'HACCP')})</span>
                    </div>
                    <p style="font-size:0.84rem; color:#CBD5E1; margin:4px 0;"><b>Observation:</b> {v.get('observation', '')}</p>
                    <p style="font-size:0.84rem; color:#34D399; margin:2px 0 0 0;"><b>Corrective Action:</b> {v.get('action', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No compliance violations detected. Kitchen meets clean standards.")
            
        # Summary & Export
        st.markdown(f"""
        <div class="fv-callout fv-callout-info">
            <b>Auditor Summary:</b> {result.get('summary', 'Standard commercial compliance audit complete.')}
        </div>
        """, unsafe_allow_html=True)
        
        # Downloadable Inspection Report
        report_text = f"""# COMMERCIAL KITCHEN HYGIENE AUDIT REPORT
Facility: {facility_type}
Compliance Score: {score}% ({grade})
Status: {status}

## INDICATORS
- Chef Hat / Hairnet: {hat_stat}
- Glove Protocol: {glove_stat}
- Surface Sanitization: {clean_stat}
- Cross-Contamination: {cross_stat}

## VIOLATION LOGS
"""
        for v in violations:
            report_text += f"\n- [{v.get('severity', 'Minor')}] {v.get('issue')}: {v.get('observation')} (Action: {v.get('action')})"
        report_text += f"\n\n## SUMMARY\n{result.get('summary', '')}\n"
        
        st.download_button(
            label="📥 Download Official HACCP Audit Report",
            data=report_text,
            file_name="kitchen_hygiene_audit_report.md",
            mime="text/markdown",
            use_container_width=True
        )

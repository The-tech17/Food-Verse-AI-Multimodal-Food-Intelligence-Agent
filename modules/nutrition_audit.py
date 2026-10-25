"""
Food Verse AI - Tab 1: Food Recognition & Nutrition Audit (Epic 2)
Provides multimodal food recognition, portion analysis, nutritional breakdown,
interactive macro charts, allergen alerts, and composite Health Score.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from modules.sample_data import SAMPLE_DISHES, get_sample_image

def calculate_dri_percentages(calories, protein, carbs, fats, fiber, sodium):
    """Computes percentage of typical Daily Reference Intake (2000 kcal baseline)."""
    return {
        "Calories": min(100, round((calories / 2000) * 100, 1)),
        "Protein": min(100, round((protein / 60) * 100, 1)),
        "Carbohydrates": min(100, round((carbs / 275) * 100, 1)),
        "Fats": min(100, round((fats / 78) * 100, 1)),
        "Fiber": min(100, round((fiber / 28) * 100, 1)),
        "Sodium": min(100, round((sodium / 2300) * 100, 1))
    }

def render_macro_charts(protein: float, carbs: float, fats: float, fiber: float, calories: int, sodium: int):
    """Renders Plotly interactive donut chart and DRI comparison bar chart."""
    col1, col2 = st.columns([1, 1])
    
    # Donut Chart for Caloric Contribution
    # 1g Protein = 4 kcal, 1g Carbs = 4 kcal, 1g Fat = 9 kcal
    prot_cals = protein * 4
    carb_cals = carbs * 4
    fat_cals = fats * 9
    total_macro_cals = max(1, prot_cals + carb_cals + fat_cals)
    
    with col1:
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Protein (4 kcal/g)', 'Carbohydrates (4 kcal/g)', 'Healthy Fats (9 kcal/g)'],
            values=[prot_cals, carb_cals, fat_cals],
            hole=0.62,
            marker=dict(colors=['#10B981', '#3B82F6', '#F59E0B'], line=dict(color='#0F172A', width=2)),
            textinfo='percent',
            hoverinfo='label+value',
            direction='clockwise'
        )])
        fig_donut.update_layout(
            title=dict(text="<b>Caloric Macro Ratio</b>", font=dict(color="#F8FAFC", size=15)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
            annotations=[dict(text=f'<b>{calories}</b><br><span style="font-size:11px">kcal</span>', x=0.5, y=0.5, font_size=18, font_color="#10B981", showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Horizontal Bar Chart for % Daily Reference Intake (DRI)
    with col2:
        dri = calculate_dri_percentages(calories, protein, carbs, fats, fiber, sodium)
        categories = list(dri.keys())
        percentages = list(dri.values())
        
        # Color scale based on limits
        bar_colors = ['#10B981', '#34D399', '#3B82F6', '#F59E0B', '#10B981', '#F43F5E' if dri['Sodium'] > 50 else '#94A3B8']
        
        fig_bar = go.Figure(go.Bar(
            x=percentages,
            y=categories,
            orientation='h',
            marker=dict(color=bar_colors, opacity=0.85, line=dict(color='rgba(255,255,255,0.2)', width=1)),
            text=[f"{p}%" for p in percentages],
            textposition='auto',
        ))
        fig_bar.update_layout(
            title=dict(text="<b>% Daily Reference Intake (DRI)</b>", font=dict(color="#F8FAFC", size=15)),
            xaxis=dict(title="% of Daily Target (2000 kcal)", range=[0, max(110, max(percentages) + 15)], gridcolor='rgba(255,255,255,0.06)', color="#94A3B8"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.06)', color="#94A3B8"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=40, b=10),
            height=300
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def render_nutrition_tab(ai_engine):
    """Main renderer for Food Recognition & Nutrition Audit."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">🍽️ Food Recognition & Nutrition Audit</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            Multimodal deep vision analysis for dish identification, ingredient breakdown, portion weight estimation, and clinical nutritional profiling.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title">📷 Upload Meal Image or Select Preset</p>', unsafe_allow_html=True)
        
        # Preset buttons for 1-click test
        st.caption("⚡ Quick Demo Presets:")
        preset_cols = st.columns(3)
        selected_preset = None
        with preset_cols[0]:
            if st.button("🥗 Salmon Bowl", key="preset_salmon", use_container_width=True):
                selected_preset = "salmon_bowl"
        with preset_cols[1]:
            if st.button("🍔 Cheeseburger", key="preset_burger", use_container_width=True):
                selected_preset = "cheeseburger"
        with preset_cols[2]:
            if st.button("🥑 Buddha Bowl", key="preset_buddha", use_container_width=True):
                selected_preset = "vegan_buddha"

        if selected_preset:
            st.session_state["tab1_active_preset"] = selected_preset
            st.session_state["tab1_uploaded_file"] = None

        uploaded_file = st.file_uploader(
            "Upload dish photograph (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="food_image_uploader"
        )
        if uploaded_file:
            st.session_state["tab1_uploaded_file"] = uploaded_file
            st.session_state["tab1_active_preset"] = None
            
        user_hint = st.text_input("Optional context/notes (e.g. 'dressing on the side', 'low sodium'):", "")
        
        # Determine image to show
        display_img = None
        preset_key = st.session_state.get("tab1_active_preset", "salmon_bowl")
        
        if st.session_state.get("tab1_uploaded_file") is not None:
            try:
                display_img = Image.open(st.session_state["tab1_uploaded_file"])
            except Exception as e:
                st.error(f"Error opening image: {e}")
        else:
            display_img = get_sample_image(preset_key)
            
        if display_img:
            st.image(display_img, caption="Meal Visual Input for Multimodal Vision Inference", use_container_width=True)
            
        analyze_clicked = st.button("🔍 Run Multimodal Nutrition Audit", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_output:
        # Check if we should trigger analysis or use cached state
        if analyze_clicked or "tab1_result" not in st.session_state:
            with st.spinner("🤖 Multimodal Vision Transformer parsing ingredients and calculating macros..."):
                if st.session_state.get("tab1_uploaded_file") is not None and ai_engine.provider != "Demo":
                    result = ai_engine.analyze_nutrition(display_img, user_hint)
                else:
                    # If preset or demo
                    result = SAMPLE_DISHES.get(preset_key, SAMPLE_DISHES["salmon_bowl"])
                st.session_state["tab1_result"] = result
        else:
            result = st.session_state["tab1_result"]
            
        # Display Result Card
        title = result.get("title", "Detected Meal")
        cuisine = result.get("cuisine", "International")
        portion = result.get("portion_size", "Single Serving")
        score = result.get("health_score", 85)
        score_rating = result.get("health_rating", "High Quality")
        
        score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#F43F5E")
        
        st.markdown(f"""
        <div class="fv-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin:0; font-size:1.4rem; color:#FFFFFF;">{title}</h3>
                    <div style="margin-top:6px; display:flex; gap:8px; flex-wrap:wrap;">
                        <span class="fv-tag">{cuisine}</span>
                        <span class="fv-tag" style="background:rgba(148, 163, 184, 0.15); color:#E2E8F0; border-color:rgba(148, 163, 184, 0.3);">Portion: {portion}</span>
                    </div>
                </div>
                <div class="fv-score-container" style="border-color:{score_color}; padding:8px 14px; margin:0;">
                    <div class="fv-score-circle" style="border-color:{score_color}; width:56px; height:56px; min-width:56px;">
                        <span class="fv-score-number" style="color:{score_color}; font-size:1.3rem;">{score}</span>
                    </div>
                    <div>
                        <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">HEALTH SCORE</div>
                        <div style="font-size:0.9rem; font-weight:700; color:{score_color};">{score_rating}</div>
                    </div>
                </div>
            </div>
            
            <div class="fv-metric-grid" style="margin-top:18px;">
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Energy</div>
                    <div class="fv-metric-val" style="color:#10B981;">{result.get('calories', 0)}<span class="fv-metric-unit">kcal</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Protein</div>
                    <div class="fv-metric-val">{result.get('protein', 0)}<span class="fv-metric-unit">g</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Carbohydrates</div>
                    <div class="fv-metric-val">{result.get('carbs', 0)}<span class="fv-metric-unit">g</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Total Fats</div>
                    <div class="fv-metric-val">{result.get('fats', 0)}<span class="fv-metric-unit">g</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Dietary Fiber</div>
                    <div class="fv-metric-val" style="color:#34D399;">{result.get('fiber', 0)}<span class="fv-metric-unit">g</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Sodium</div>
                    <div class="fv-metric-val">{result.get('sodium', 0)}<span class="fv-metric-unit">mg</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Macro charts
        render_macro_charts(
            protein=float(result.get("protein", 30)),
            carbs=float(result.get("carbs", 40)),
            fats=float(result.get("fats", 15)),
            fiber=float(result.get("fiber", 5)),
            calories=int(result.get("calories", 500)),
            sodium=int(result.get("sodium", 400))
        )
        
        # Ingredients & Allergens in tabs/columns
        tab_ingr, tab_allergens, tab_science = st.tabs(["🥗 Ingredient Breakdown", "⚠️ Allergen Alerts", "🔬 Food Science Notes"])
        
        with tab_ingr:
            ingredients = result.get("ingredients", [])
            if ingredients:
                ingr_df = pd.DataFrame(ingredients)
                st.dataframe(
                    ingr_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Detected Ingredient", width="medium"),
                        "weight": st.column_config.TextColumn("Portion", width="small"),
                        "calories": st.column_config.NumberColumn("Est. Calories", format="%d kcal", width="small")
                    }
                )
            else:
                st.info("No itemized ingredient data detected.")
                
        with tab_allergens:
            allergens = result.get("allergens", [])
            if allergens:
                for a in allergens:
                    sev = a.get("severity", "Medium")
                    badge_style = "fv-callout-danger" if sev == "High" else "fv-callout-warning"
                    st.markdown(f"""
                    <div class="fv-callout {badge_style}">
                        <b>Allergen Detected: {a.get('allergen', 'Unknown')}</b> (Severity: {sev})<br>
                        <span style="font-size:0.85rem; opacity:0.9;">Source: {a.get('source', 'Dish components')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="fv-callout fv-callout-success">✅ No standard major FDA allergens flagged in this dish.</div>', unsafe_allow_html=True)
                
            dietary_tags = result.get("dietary_tags", [])
            if dietary_tags:
                st.markdown('<p style="font-size:0.85rem; color:#94A3B8; margin-top:8px; font-weight:600;">DIETARY CLASSIFICATIONS:</p>', unsafe_allow_html=True)
                tags_html = " ".join([f'<span class="fv-tag fv-tag-safe">{tag}</span>' for tag in dietary_tags])
                st.markdown(tags_html, unsafe_allow_html=True)

        with tab_science:
            st.markdown(f"""
            <div class="fv-callout fv-callout-info">
                <b>Clinical Nutrition Analysis:</b><br>
                {result.get('science_notes', 'Optimal macronutrient balance supporting sustained glycemic control.')}
            </div>
            """, unsafe_allow_html=True)

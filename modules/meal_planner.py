"""
Food Verse AI - Tab 5: Personalized Meal Planner & TDEE Engine (Epic 5)
Calculates clinical BMR (Mifflin-St Jeor) and TDEE caloric targets,
generating an adaptive 7-day meal schedule with an automated grocery shopping list.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_bmr_and_tdee(age: int, gender: str, weight_kg: float, height_cm: float, activity: str, goal: str, diet: str):
    """
    Computes BMR using the Mifflin-St Jeor equation and TDEE using standard PAL multipliers.
    Calibrates macronutrient targets based on goal and diet constraints.
    """
    # Mifflin-St Jeor formula
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    activity_factors = {
        "Sedentary (Little or no exercise)": 1.2,
        "Lightly Active (Exercise 1-3 days/week)": 1.375,
        "Moderately Active (Exercise 3-5 days/week)": 1.55,
        "Very Active (Hard training 6-7 days/week)": 1.725,
        "Extremely Active (Athletic training / physical labor)": 1.9
    }
    pal = activity_factors.get(activity, 1.375)
    tdee = round(bmr * pal)
    
    # Goal Adjustment
    goal_deltas = {
        "Fat Loss (Moderate -300 kcal)": -300,
        "Aggressive Fat Loss (-500 kcal)": -500,
        "Maintenance (Sustain Energy Balance)": 0,
        "Clean Muscle Gain (+300 kcal)": 300,
        "Athletic Mass Surplus (+500 kcal)": 500
    }
    delta = goal_deltas.get(goal, -300)
    target_cals = max(1200, tdee + delta)
    
    # Calibrate Macros
    if "keto" in diet.lower():
        # 5% carbs, 25% protein, 70% fats
        prot_g = round((target_cals * 0.25) / 4)
        fat_g = round((target_cals * 0.70) / 9)
        carb_g = round((target_cals * 0.05) / 4)
    elif "high protein" in diet.lower() or "muscle" in goal.lower():
        # High protein: 2.0g per kg bodyweight
        prot_g = round(min(weight_kg * 2.2, target_cals * 0.35 / 4))
        fat_g = round((target_cals * 0.25) / 9)
        carb_g = round((target_cals - (prot_g * 4 + fat_g * 9)) / 4)
    elif "diabetic" in diet.lower():
        # Controlled low-GI: 35% carbs, 30% protein, 35% healthy fats
        prot_g = round((target_cals * 0.30) / 4)
        fat_g = round((target_cals * 0.35) / 9)
        carb_g = round((target_cals * 0.35) / 4)
    else:
        # Balanced Mediterranean: 45% carbs, 25% protein, 30% fats
        prot_g = round((target_cals * 0.25) / 4)
        fat_g = round((target_cals * 0.30) / 9)
        carb_g = round((target_cals * 0.45) / 4)
        
    return {
        "bmr": round(bmr),
        "tdee": tdee,
        "target_calories": target_cals,
        "protein_g": prot_g,
        "carbs_g": carb_g,
        "fat_g": fat_g
    }

def render_meal_planner_tab(ai_engine):
    """Main renderer for Tab 5: Personalized Meal Planner."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">📊 Personalized 7-Day Meal Planner & TDEE Engine</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            Evidence-based metabolic calculation (Mifflin-St Jeor) generating an adaptive 7-day nutritional schedule with an aisle-sorted grocery shopping list.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title">👤 User Biometrics & Profile</p>', unsafe_allow_html=True)
        
        # Preset profile buttons
        st.caption("⚡ Quick Profile Presets:")
        p_cols = st.columns(3)
        with p_cols[0]:
            if st.button("👩 Sarah (Loss)", key="prof_sarah", use_container_width=True):
                st.session_state["p_age"] = 28
                st.session_state["p_gender"] = "Female"
                st.session_state["p_weight"] = 65.0
                st.session_state["p_height"] = 168.0
                st.session_state["p_activity"] = "Moderately Active (Exercise 3-5 days/week)"
                st.session_state["p_goal"] = "Fat Loss (Moderate -300 kcal)"
                st.session_state["p_diet"] = "Mediterranean"
        with p_cols[1]:
            if st.button("👨 Alex (Muscle)", key="prof_alex", use_container_width=True):
                st.session_state["p_age"] = 32
                st.session_state["p_gender"] = "Male"
                st.session_state["p_weight"] = 82.0
                st.session_state["p_height"] = 182.0
                st.session_state["p_activity"] = "Very Active (Hard training 6-7 days/week)"
                st.session_state["p_goal"] = "Clean Muscle Gain (+300 kcal)"
                st.session_state["p_diet"] = "High Protein"
        with p_cols[2]:
            if st.button("🧑 David (Diabetic)", key="prof_david", use_container_width=True):
                st.session_state["p_age"] = 48
                st.session_state["p_gender"] = "Male"
                st.session_state["p_weight"] = 88.0
                st.session_state["p_height"] = 175.0
                st.session_state["p_activity"] = "Lightly Active (Exercise 1-3 days/week)"
                st.session_state["p_goal"] = "Fat Loss (Moderate -300 kcal)"
                st.session_state["p_diet"] = "Diabetic-Friendly (Low GI)"

        # Input Form
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age (years):", min_value=14, max_value=100, value=st.session_state.get("p_age", 28))
            gender = st.selectbox("Biological Gender:", ["Female", "Male"], index=0 if st.session_state.get("p_gender", "Female") == "Female" else 1)
            weight = st.number_input("Weight (kg):", min_value=35.0, max_value=250.0, value=float(st.session_state.get("p_weight", 65.0)), step=0.5)
        with c2:
            height = st.number_input("Height (cm):", min_value=120.0, max_value=230.0, value=float(st.session_state.get("p_height", 168.0)), step=0.5)
            goal = st.selectbox("Fitness & Weight Goal:", [
                "Fat Loss (Moderate -300 kcal)",
                "Aggressive Fat Loss (-500 kcal)",
                "Maintenance (Sustain Energy Balance)",
                "Clean Muscle Gain (+300 kcal)",
                "Athletic Mass Surplus (+500 kcal)"
            ], index=0)
            diet = st.selectbox("Dietary Pattern:", [
                "Mediterranean",
                "High Protein",
                "Diabetic-Friendly (Low GI)",
                "Vegan / Plant-Based",
                "Vegetarian",
                "Keto / Low-Carb",
                "Gluten-Free Clean Eating"
            ], index=0)

        activity = st.selectbox("Physical Activity Level:", [
            "Sedentary (Little or no exercise)",
            "Lightly Active (Exercise 1-3 days/week)",
            "Moderately Active (Exercise 3-5 days/week)",
            "Very Active (Hard training 6-7 days/week)",
            "Extremely Active (Athletic training / physical labor)"
        ], index=2)

        # Compute targets immediately
        targets = calculate_bmr_and_tdee(age, gender, weight, height, activity, goal, diet)
        
        st.markdown('<hr style="border-color:rgba(255,255,255,0.06); margin:16px 0;">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title" style="font-size:1rem;">📐 Computed Metabolic Baseline</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="fv-metric-grid">
            <div class="fv-metric-item">
                <div class="fv-metric-label">Basal BMR</div>
                <div class="fv-metric-val">{targets['bmr']}<span class="fv-metric-unit">kcal</span></div>
            </div>
            <div class="fv-metric-item">
                <div class="fv-metric-label">TDEE Burn</div>
                <div class="fv-metric-val">{targets['tdee']}<span class="fv-metric-unit">kcal</span></div>
            </div>
            <div class="fv-metric-item" style="border-color:#10B981;">
                <div class="fv-metric-label" style="color:#34D399;">Target Calories</div>
                <div class="fv-metric-val" style="color:#10B981;">{targets['target_calories']}<span class="fv-metric-unit">kcal</span></div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-around; background:rgba(15,23,42,0.6); padding:10px; border-radius:10px; font-size:0.85rem; color:#94A3B8;">
            <span>🥩 Protein: <b style="color:#F8FAFC;">{targets['protein_g']}g</b></span>
            <span>🍚 Carbs: <b style="color:#F8FAFC;">{targets['carbs_g']}g</b></span>
            <span>🥑 Fats: <b style="color:#F8FAFC;">{targets['fat_g']}g</b></span>
        </div>
        """, unsafe_allow_html=True)

        generate_plan_clicked = st.button("🗓️ Generate Adaptive 7-Day Plan", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_output:
        profile_dict = {
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "goal": goal,
            "diet": diet,
            "activity": activity
        }
        
        if generate_plan_clicked or "tab5_plan" not in st.session_state:
            with st.spinner("🥗 Sports Nutritionist synthesizing 7-day adaptive caloric schedule and grocery list..."):
                plan = ai_engine.generate_adaptive_meal_plan(profile_dict, targets)
                st.session_state["tab5_plan"] = plan
        else:
            plan = st.session_state["tab5_plan"]
            
        overview = plan.get("overview", "Custom 7-day dietary protocol.")
        st.markdown(f"""
        <div class="fv-callout fv-callout-info" style="margin-top:0;">
            <b>Personalized Dietary Strategy:</b><br>{overview}
        </div>
        """, unsafe_allow_html=True)
        
        tab_schedule, tab_grocery = st.tabs(["📅 7-Day Meal Schedule", "🛒 Automated Grocery Shopping List"])
        
        with tab_schedule:
            schedule = plan.get("weekly_schedule", [])
            for day_data in schedule:
                day_title = day_data.get("day", "Day")
                day_cals = day_data.get("total_calories", targets['target_calories'])
                
                with st.expander(f"📌 {day_title} — Target: {day_cals} kcal", expanded=(day_title.startswith("Day 1"))):
                    b = day_data.get("breakfast", {})
                    l = day_data.get("lunch", {})
                    d = day_data.get("dinner", {})
                    s = day_data.get("snack", {})
                    
                    st.markdown(f"""
                    <div style="font-size:0.88rem; line-height:1.6;">
                        <p>🍳 <b>Breakfast ({b.get('calories', 0)} kcal | {b.get('protein', '')} protein):</b><br>{b.get('name', 'Oatmeal & Eggs')}</p>
                        <p>🥗 <b>Lunch ({l.get('calories', 0)} kcal | {l.get('protein', '')} protein):</b><br>{l.get('name', 'Quinoa Salmon Bowl')}</p>
                        <p>🍽️ <b>Dinner ({d.get('calories', 0)} kcal | {d.get('protein', '')} protein):</b><br>{d.get('name', 'Herb Chicken & Vegetables')}</p>
                        <p>🍎 <b>Snack ({s.get('calories', 0)} kcal | {s.get('protein', '')} protein):</b><br>{s.get('name', 'Almonds & Fruit')}</p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_grocery:
            grocery_list = plan.get("grocery_list", {})
            st.markdown('<p style="font-size:0.85rem; color:#94A3B8; font-weight:600;">SUPERMARKET AISLE CHECKLIST:</p>', unsafe_allow_html=True)
            
            g_cols = st.columns(2)
            dept_names = list(grocery_list.keys())
            
            for idx, dept in enumerate(dept_names):
                target_col = g_cols[idx % 2]
                with target_col:
                    st.markdown(f"""
                    <div class="fv-card" style="padding:14px; margin-bottom:12px;">
                        <b style="color:#10B981; font-size:0.95rem;">🏬 {dept}</b>
                    """, unsafe_allow_html=True)
                    for item in grocery_list[dept]:
                        st.checkbox(item, key=f"groc_{dept}_{item}", value=False)
                    st.markdown('</div>', unsafe_allow_html=True)

        # Download / Export Section
        st.markdown('<hr style="border-color:rgba(255,255,255,0.06); margin:18px 0;">', unsafe_allow_html=True)
        
        # Build Export Markdown
        export_md = f"""# FOOD VERSE AI - 7-DAY PERSONALIZED NUTRITION BLUEPRINT
User Profile: {age}yo {gender} | {weight}kg, {height}cm
Fitness Goal: {goal}
Dietary Pattern: {diet}
Basal Metabolic Rate (BMR): {targets['bmr']} kcal/day
Total Daily Energy Expenditure (TDEE): {targets['tdee']} kcal/day
Calibrated Daily Energy Target: {targets['target_calories']} kcal/day
Macronutrient Distribution: Protein: {targets['protein_g']}g | Carbs: {targets['carbs_g']}g | Fats: {targets['fat_g']}g

## STRATEGY OVERVIEW
{overview}

## 7-DAY MEAL SCHEDULE
"""
        for day in schedule:
            export_md += f"\n### {day.get('day')} ({day.get('total_calories')} kcal)\n"
            export_md += f"- Breakfast: {day.get('breakfast', {}).get('name')} ({day.get('breakfast', {}).get('calories')} kcal)\n"
            export_md += f"- Lunch: {day.get('lunch', {}).get('name')} ({day.get('lunch', {}).get('calories')} kcal)\n"
            export_md += f"- Dinner: {day.get('dinner', {}).get('name')} ({day.get('dinner', {}).get('calories')} kcal)\n"
            export_md += f"- Snack: {day.get('snack', {}).get('name')} ({day.get('snack', {}).get('calories')} kcal)\n"

        export_md += "\n## AISLE-ORGANIZED GROCERY SHOPPING LIST\n"
        for dept, items in grocery_list.items():
            export_md += f"\n### {dept}\n"
            for itm in items:
                export_md += f"- [ ] {itm}\n"
                
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="📥 Download 7-Day Plan (Markdown)",
                data=export_md,
                file_name="foodverse_7day_meal_plan.md",
                mime="text/markdown",
                use_container_width=True
            )
        with d_col2:
            # Simple CSV export of meals
            csv_rows = []
            for d in schedule:
                csv_rows.append({"Day": d.get("day"), "Meal": "Breakfast", "Item": d.get("breakfast", {}).get("name"), "Calories": d.get("breakfast", {}).get("calories")})
                csv_rows.append({"Day": d.get("day"), "Meal": "Lunch", "Item": d.get("lunch", {}).get("name"), "Calories": d.get("lunch", {}).get("calories")})
                csv_rows.append({"Day": d.get("day"), "Meal": "Dinner", "Item": d.get("dinner", {}).get("name"), "Calories": d.get("dinner", {}).get("calories")})
                csv_rows.append({"Day": d.get("day"), "Meal": "Snack", "Item": d.get("snack", {}).get("name"), "Calories": d.get("snack", {}).get("calories")})
            csv_df = pd.DataFrame(csv_rows)
            st.download_button(
                label="📊 Download Meal Schedule (CSV)",
                data=csv_df.to_csv(index=False),
                file_name="foodverse_meal_schedule.csv",
                mime="text/csv",
                use_container_width=True
            )

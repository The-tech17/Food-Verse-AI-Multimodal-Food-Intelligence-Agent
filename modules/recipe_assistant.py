"""
Food Verse AI - Tab 4: Smart Kitchen Recipe Assistant (Epic 4)
Pantry inventory manager generating creative, nutritious recipes with cooking times,
difficulty levels, step-by-step instructions, and ingredient substitutions.
"""

import streamlit as st
from modules.sample_data import SAMPLE_PANTRY_PRESETS, SAMPLE_RECIPES

def render_recipe_tab(ai_engine):
    """Main renderer for Smart Kitchen Recipe Assistant."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin:0; font-weight:800; color:#F8FAFC;">🍳 Smart Kitchen Recipe Assistant</h2>
        <p style="color:#94A3B8; font-size:0.95rem; margin-top:4px;">
            AI culinary intelligence transforming surplus and available pantry ingredients into nutritious, chef-crafted recipes with smart substitutions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title">🧺 Your Pantry Inventory</p>', unsafe_allow_html=True)
        
        # Preset buttons for 1-click test
        st.caption("⚡ Quick Pantry Presets:")
        p_cols = st.columns(2)
        with p_cols[0]:
            if st.button("🥗 Mediterranean", key="preset_pantry_med", use_container_width=True):
                st.session_state["pantry_items"] = SAMPLE_PANTRY_PRESETS["Mediterranean Wellness"]
            if st.button("🥫 Student Budget", key="preset_pantry_budget", use_container_width=True):
                st.session_state["pantry_items"] = SAMPLE_PANTRY_PRESETS["Pantry Cleanout (Student Budget)"]
        with p_cols[1]:
            if st.button("💪 High Protein", key="preset_pantry_protein", use_container_width=True):
                st.session_state["pantry_items"] = SAMPLE_PANTRY_PRESETS["High-Protein Muscle Prep"]
            if st.button("🌱 Vegan Power", key="preset_pantry_vegan", use_container_width=True):
                st.session_state["pantry_items"] = SAMPLE_PANTRY_PRESETS["Plant-Powered Vegan"]

        # Default pantry if empty
        if "pantry_items" not in st.session_state or not st.session_state["pantry_items"]:
            st.session_state["pantry_items"] = SAMPLE_PANTRY_PRESETS["Mediterranean Wellness"]

        # Multi-select or add items
        current_items = st.multiselect(
            "Active Pantry Ingredients:",
            options=sorted(list(set(st.session_state["pantry_items"] + [
                "Chicken Breast", "Salmon Fillet", "Eggs", "Tofu", "Canned Tuna", "Ground Turkey",
                "Quinoa", "Brown Rice", "Oats", "Pasta", "Chickpeas", "Black Beans",
                "Baby Spinach", "Broccoli", "Cherry Tomatoes", "Avocado", "Bell Peppers", "Mushrooms",
                "Greek Yogurt", "Feta Cheese", "Cheddar", "Almond Milk", "Butter",
                "Olive Oil", "Garlic", "Lemon", "Soy Sauce", "Ginger", "Chili Flakes"
            ]))),
            default=st.session_state["pantry_items"],
            key="pantry_multiselect"
        )
        st.session_state["pantry_items"] = current_items

        # Custom item text add
        c_add1, c_add2 = st.columns([3, 1])
        with c_add1:
            custom_item = st.text_input("Add custom pantry item:", placeholder="e.g., Zucchini, Coconut milk", label_visibility="collapsed")
        with c_add2:
            if st.button("➕ Add", use_container_width=True) and custom_item.strip():
                if custom_item.strip() not in st.session_state["pantry_items"]:
                    st.session_state["pantry_items"].append(custom_item.strip())
                    st.rerun()

        st.markdown('<hr style="border-color:rgba(255,255,255,0.06); margin:16px 0;">', unsafe_allow_html=True)
        st.markdown('<p class="fv-card-title" style="font-size:1rem;">⚙️ Recipe Customization</p>', unsafe_allow_html=True)
        
        pref_col1, pref_col2 = st.columns(2)
        with pref_col1:
            meal_type = st.selectbox("Meal Category:", ["Dinner", "Lunch", "Breakfast", "High-Protein Snack", "Post-Workout Fuel"])
            skill_level = st.selectbox("Culinary Skill:", ["Beginner Friendly", "Intermediate", "Master Chef / Gourmet"])
        with pref_col2:
            max_time = st.selectbox("Max Time Limit:", ["15 mins (Quick)", "20 mins", "30 mins", "45 mins", "60+ mins"])
            diet_pref = st.selectbox("Diet Style:", ["Balanced", "High Protein", "Mediterranean", "Keto / Low-Carb", "Vegan", "Gluten-Free"])

        generate_clicked = st.button("✨ Generate AI Chef Recipe", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_output:
        preferences = {
            "meal_type": meal_type,
            "skill_level": skill_level,
            "max_time": max_time,
            "diet": diet_pref
        }
        
        if generate_clicked or "tab4_recipe" not in st.session_state:
            with st.spinner("👨‍🍳 Master Chef crafting optimal recipe matching your pantry and nutritional goals..."):
                if ai_engine.provider != "Demo":
                    recipe = ai_engine.generate_smart_recipe(st.session_state["pantry_items"], preferences)
                else:
                    recipe = SAMPLE_RECIPES["mediterranean"]
                st.session_state["tab4_recipe"] = recipe
        else:
            recipe = st.session_state["tab4_recipe"]
            
        # Display Generated Recipe
        title = recipe.get("title", "Gourmet Dish")
        prep_time = recipe.get("prep_time", "10 mins")
        cook_time = recipe.get("cook_time", "15 mins")
        total_time = recipe.get("total_time", "25 mins")
        difficulty = recipe.get("difficulty", "Easy")
        servings = recipe.get("servings", 2)
        cals = recipe.get("calories_per_serving", 450)
        macros = recipe.get("macros", {"protein": "35g", "carbs": "30g", "fats": "18g", "fiber": "6g"})
        
        st.markdown(f"""
        <div class="fv-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                <div>
                    <h3 style="margin:0; font-size:1.4rem; color:#FFFFFF;">{title}</h3>
                    <div style="margin-top:6px; display:flex; gap:8px; flex-wrap:wrap;">
                        <span class="fv-tag" style="background:rgba(16, 185, 129, 0.15); color:#34D399;">⏱️ Total: {total_time}</span>
                        <span class="fv-tag" style="background:rgba(59, 130, 246, 0.15); color:#93C5FD;">👥 Servings: {servings}</span>
                        <span class="fv-tag" style="background:rgba(245, 158, 11, 0.15); color:#FCD34D;">⭐ Difficulty: {difficulty}</span>
                    </div>
                </div>
            </div>
            
            <div class="fv-metric-grid" style="margin-top:16px;">
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Per Serving</div>
                    <div class="fv-metric-val" style="color:#10B981;">{cals}<span class="fv-metric-unit">kcal</span></div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Protein</div>
                    <div class="fv-metric-val">{macros.get('protein', '30g')}</div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Carbs</div>
                    <div class="fv-metric-val">{macros.get('carbs', '35g')}</div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Fats</div>
                    <div class="fv-metric-val">{macros.get('fats', '15g')}</div>
                </div>
                <div class="fv-metric-item">
                    <div class="fv-metric-label">Fiber</div>
                    <div class="fv-metric-val" style="color:#34D399;">{macros.get('fiber', '5g')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for Ingredients, Steps, and Substitutions
        tab_prep, tab_steps, tab_subs = st.tabs(["🛒 Ingredients Checklist", "👨‍🍳 Cooking Instructions", "🔄 Smart Substitutions"])
        
        with tab_prep:
            st.markdown('<p style="font-size:0.85rem; color:#94A3B8; font-weight:600;">REQUIRED INGREDIENTS:</p>', unsafe_allow_html=True)
            for idx, ingr in enumerate(recipe.get("ingredients", [])):
                st.checkbox(f"**{ingr}**", key=f"rec_ing_{idx}", value=True)
                
            waste_tip = recipe.get("waste_reduction_tip")
            if waste_tip:
                st.markdown(f"""
                <div class="fv-callout fv-callout-success" style="margin-top:16px;">
                    🌱 <b>Zero-Waste Food Science Tip:</b><br>{waste_tip}
                </div>
                """, unsafe_allow_html=True)

        with tab_steps:
            st.markdown('<p style="font-size:0.85rem; color:#94A3B8; font-weight:600;">STEP-BY-STEP CHEF METHOD:</p>', unsafe_allow_html=True)
            for s_idx, step in enumerate(recipe.get("steps", []), 1):
                st.markdown(f"""
                <div style="display:flex; gap:12px; margin-bottom:12px; align-items:flex-start;">
                    <div style="background:#10B981; color:#0F172A; font-weight:800; min-width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.85rem;">
                        {s_idx}
                    </div>
                    <div style="font-size:0.92rem; color:#E2E8F0; line-height:1.5;">
                        {step}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_subs:
            subs = recipe.get("substitutions", [])
            if subs:
                for sub in subs:
                    st.markdown(f"""
                    <div class="fv-callout fv-callout-info">
                        <b>Missing or Allergy swap: {sub.get('ingredient')}</b><br>
                        <span>👉 <b>Substitute with:</b> {sub.get('substitution')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("All pantry items align directly with standard ingredients.")

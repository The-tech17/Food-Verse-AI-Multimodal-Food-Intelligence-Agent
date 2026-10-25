"""
Food Verse AI - Multimodal Food Intelligence Agent
Skill Wallet Capstone Project 3

A production-ready multimodal food intelligence platform delivering:
1. Food Recognition & Nutrition Audit (Epic 2)
2. Food Freshness & Spoilage Diagnostic (Epic 3)
3. Commercial Kitchen Hygiene & Food Safety Compliance (Epic 4)
4. Smart Kitchen Recipe Assistant (Epic 4)
5. Personalized 7-Day Meal Planner & TDEE Engine (Epic 5)
6. Food Science & System Architecture Engine
"""

import os
import streamlit as st
from PIL import Image

# Initialize AI Engine and Modules
from modules.ai_engine import FoodVerseAIEngine, GEMINI_AVAILABLE, GROQ_AVAILABLE
from modules.nutrition_audit import render_nutrition_tab
from modules.freshness_diagnostic import render_freshness_tab
from modules.hygiene_compliance import render_hygiene_tab
from modules.recipe_assistant import render_recipe_tab
from modules.meal_planner import render_meal_planner_tab
from modules.system_architecture import render_architecture_tab

# Page Configuration
st.set_page_config(
    page_title="Food Verse AI - Multimodal Food Intelligence Agent",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and inject custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =============================================================================
# SIDEBAR: Persona, API Key Management, and Operational Controls
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <span style="font-size:2.2rem;">🥗</span>
        <div>
            <h2 style="margin:0; font-size:1.25rem; font-weight:800; color:#FFFFFF;">FoodVerse AI</h2>
            <span style="font-size:0.75rem; color:#10B981; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Multimodal Food Agent</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="fv-card" style="padding:14px; margin-bottom:16px;">', unsafe_allow_html=True)
    st.markdown('<p class="fv-card-title" style="font-size:0.9rem;">⚙️ Intelligence Provider</p>', unsafe_allow_html=True)
    
    mode_options = [
        "Standalone Showcase Mode (No Key Needed)",
        "Google Gemini (Multimodal Vision)",
        "Groq Cloud (Llama 3.2 Vision)"
    ]
    
    selected_mode = st.selectbox(
        "Inference Engine:",
        mode_options,
        index=0,
        help="Select Standalone Showcase Mode for instant 1-click demonstration with zero API key dependencies, or connect your Gemini / Groq API keys."
    )
    
    gemini_key = ""
    groq_key = ""
    
    if selected_mode == "Google Gemini (Multimodal Vision)":
        env_gemini = os.getenv("GEMINI_API_KEY", "")
        gemini_key = st.text_input(
            "Gemini API Key:",
            value=env_gemini,
            type="password",
            placeholder="AIzaSy...",
            help="Your Google Gemini API key. Stored only in session memory."
        )
        if not gemini_key:
            st.warning("⚠️ No Gemini API key detected. Analysis will automatically use the standalone demonstration engine.")
            provider_tag = "Demo"
        else:
            provider_tag = "Google Gemini"
            st.success("✅ Gemini API Key Loaded")
            
    elif selected_mode == "Groq Cloud (Llama 3.2 Vision)":
        env_groq = os.getenv("GROQ_API_KEY", "")
        groq_key = st.text_input(
            "Groq API Key:",
            value=env_groq,
            type="password",
            placeholder="gsk_...",
            help="Your Groq Cloud API key. Stored only in session memory."
        )
        if not groq_key:
            st.warning("⚠️ No Groq API key detected. Analysis will automatically use the standalone demonstration engine.")
            provider_tag = "Demo"
        else:
            provider_tag = "Groq"
            st.success("✅ Groq API Key Loaded")
    else:
        provider_tag = "Demo"
        st.markdown("""
        <div style="font-size:0.8rem; color:#34D399; margin-top:4px;">
            ✨ <b>Showcase Mode Active:</b> Pre-loaded with high-fidelity food vision models & datasets. Ready for 1-click evaluation!
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Instantiate unified AI engine
    ai_engine = FoodVerseAIEngine(
        provider=provider_tag,
        gemini_key=gemini_key,
        groq_key=groq_key
    )

    # Status Pill
    status_text = "Connected (Gemini 2.5 Flash)" if provider_tag == "Google Gemini" else ("Connected (Groq Vision)" if provider_tag == "Groq" else "Showcase Simulation Active")
    st.markdown(f"""
    <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:10px 14px; margin-bottom:16px;">
        <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">Engine Telemetry</div>
        <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
            <div style="width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981;"></div>
            <span style="font-size:0.85rem; font-weight:600; color:#F8FAFC;">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Capstone Info
    st.markdown("""
    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.5; border-top:1px solid rgba(255,255,255,0.06); padding-top:14px;">
        <b style="color:#F8FAFC;">Skill Wallet Capstone Project 3</b><br>
        Food Science & Multimodal AI Agent<br>
        Version: 3.2.0 • Production Ready
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Session Cache", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# =============================================================================
# HERO BANNER
# =============================================================================
st.markdown("""
<div class="fv-hero">
    <div class="fv-badge-capsule">
        <span>✨ Skill Wallet Capstone Project 3</span>
        <span>•</span>
        <span>Multimodal Food Intelligence Agent</span>
    </div>
    <h1 class="fv-hero-title">Food Verse AI</h1>
    <p class="fv-hero-subtitle">
        Unified multimodal intelligence platform uniting clinical nutrition audits, optical spoilage diagnostics, HACCP commercial kitchen hygiene compliance, smart pantry recipe synthesis, and adaptive metabolic meal planning.
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# CORE INTELLIGENCE PILLARS (TABS)
# =============================================================================
tab_names = [
    "🍽️ Nutrition Audit",
    "🥑 Spoilage Diagnostic",
    "🧼 Kitchen Hygiene",
    "🍳 Smart Recipe Assistant",
    "📊 Personalized Meal Planner",
    "🔬 System Architecture"
]

tabs = st.tabs(tab_names)

with tabs[0]:
    render_nutrition_tab(ai_engine)

with tabs[1]:
    render_freshness_tab(ai_engine)

with tabs[2]:
    render_hygiene_tab(ai_engine)

with tabs[3]:
    render_recipe_tab(ai_engine)

with tabs[4]:
    render_meal_planner_tab(ai_engine)

with tabs[5]:
    render_architecture_tab()
